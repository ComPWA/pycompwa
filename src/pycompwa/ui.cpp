// Copyright (c) 2017 The ComPWA Team.
// This file is part of the ComPWA framework, check
// https://github.com/ComPWA/ComPWA/license.txt for details.

#include <pybind11/iostream.h>
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>

#include <boost/archive/xml_iarchive.hpp>
#include <boost/archive/xml_oarchive.hpp>
#include <boost/property_tree/xml_parser.hpp>

#include "Core/Event.hpp"
#include "Core/FourMomentum.hpp"
#include "Core/Generator.hpp"
#include "Core/Kinematics.hpp"
#include "Core/Random.hpp"
#include "Data/Ascii/AsciiDataIO.hpp"
#include "Data/DataSet.hpp"
#include "Data/EvtGen/EvtGenGenerator.hpp"
#include "Data/Generate.hpp"
#include "Data/Root/RootDataIO.hpp"
#include "Data/Root/RootGenerator.hpp"
#include "Estimator/MinLogLH/MinLogLH.hpp"
#include "Optimizer/Minuit2/MinuitIF.hpp"
#include "Optimizer/Minuit2/MinuitResult.hpp"

#include "Core/FunctionTree/FunctionTreeIntensity.hpp"
#include "Physics/BuilderXML.hpp"
#include "Physics/HelicityFormalism/HelicityKinematics.hpp"
#include "Physics/ParticleStateTransitionKinematicsInfo.hpp"

#include "Tools/FitFractions.hpp"
#include "Tools/Plotting/RootPlotData.hpp"
#include "Tools/UpdatePTreeParameter.hpp"

namespace py = pybind11;

PYBIND11_MAKE_OPAQUE(ComPWA::ParticleList);
PYBIND11_MAKE_OPAQUE(std::vector<ComPWA::FourMomentum>);
PYBIND11_MAKE_OPAQUE(std::vector<ComPWA::Event>);

PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);

PYBIND11_MODULE(ui, m) {
  m.doc() = "pycompwa module\n"
            "---------------\n";

  // -----------------------------------------
  //      Interface to Core components
  // -----------------------------------------

  /// Reinitialize the logger with level INFO and disabled log file.
  ComPWA::Logging("INFO");
  py::class_<ComPWA::Logging, std::shared_ptr<ComPWA::Logging>>(m, "Logging")
      .def(py::init<std::string, std::string>(), "Initialize logging system",
           py::arg("log_level"), py::arg("filename") = "")
      .def_property("level", &ComPWA::Logging::getLogLevel,
                    &ComPWA::Logging::setLogLevel);

  /// Write message to ComPWA logging system.
  m.def("log", [](std::string msg) { LOG(INFO) << msg; },
        "Write string to logging system.");

  /// Redirect ComPWA log output within a python scope.
  ///
  /// \code{.py}
  /// import pycompwa.ui as pwa
  /// with pwa.log_redirect(stdout=True, stderr=True):
  ///     // all logging to printed via python
  /// \endcode
  py::add_ostream_redirect(m, "log_redirect");

  /// Redirecting stdout and stderr to python printing system.
  /// This can not be changed during runtime.
  auto redirectors = std::make_unique<
      std::pair<py::scoped_ostream_redirect, py::scoped_estream_redirect>>();
  m.attr("_ostream_redirectors") =
      py::capsule(redirectors.release(), [](void *p) {
        delete reinterpret_cast<typename decltype(redirectors)::pointer>(p);
      });

  // ------- Parameters

  py::class_<ComPWA::FitParameter<double>>(m, "FitParameter")
      .def("__repr__",
           [](const ComPWA::FitParameter<double> &x) {
             std::stringstream ss;
             ss << x;
             return ss.str();
           })
      .def_readwrite("is_fixed", &ComPWA::FitParameter<double>::IsFixed)
      .def_readwrite("value", &ComPWA::FitParameter<double>::Value)
      .def_readwrite("name", &ComPWA::FitParameter<double>::Name)
      .def_readwrite("error", &ComPWA::FitParameter<double>::Error)
      .def_readwrite("bounds", &ComPWA::FitParameter<double>::Bounds);
  m.def("log", [](const ComPWA::FitParameter<double> p) { LOG(INFO) << p; });

  py::class_<ComPWA::FitParameterList>(m, "FitParameterList");

  m.def("log",
        [](const ComPWA::FitParameterList &list) {
          for (auto x : list)
            LOG(INFO) << x;
        },
        "Print FitParameter list to logging system.");

  // ------- Parameters in ptree
  m.def(
      "update_parameter_range_by_type",
      ComPWA::Tools::updateParameterRangeByType,
      "Update parameters' range of a ptree by parameter type, e.g., Magnitude.",
      py::arg("tree"), py::arg("parameter_type"), py::arg("min"),
      py::arg("max"));
  m.def("update_parameter_range_by_name",
        ComPWA::Tools::updateParameterRangeByName,
        "Update parameters' range of a ptree by parameter name.",
        py::arg("tree"), py::arg("parameter_name"), py::arg("min"),
        py::arg("max"));
  m.def("update_parameter_value", ComPWA::Tools::updateParameterValue,
        "Update parameters' value of a ptree by parameter name.",
        py::arg("tree"), py::arg("parameter_name"), py::arg("value"));
  m.def("fix_parameter", ComPWA::Tools::fixParameter,
        "Fix parameters current value (to value) of a ptree by parameter name.",
        py::arg("tree"), py::arg("parameter_name"), py::arg("value") = -999);
  m.def(
      "release_parameter", ComPWA::Tools::releaseParameter,
      "Release parameters' value (to new value) of a ptree by parameter name.",
      py::arg("tree"), py::arg("parameter_name"), py::arg("value") = -999);
  m.def("update_parameter",
        (void (*)(boost::property_tree::ptree &, const std::string &,
                  const std::string &, double, bool, double, double, bool, bool,
                  bool)) &
            ComPWA::Tools::updateParameter,
        "Update parameters' value, range, fix status, of a ptree.",
        py::arg("tree"), py::arg("key_type"), py::arg("key_value"),
        py::arg("value"), py::arg("fix"), py::arg("min"), py::arg("max"),
        py::arg("update_value"), py::arg("update_fix"),
        py::arg("update_range"));
  m.def("update_parameter",
        (void (*)(boost::property_tree::ptree &,
                  const ComPWA::FitParameterList &)) &
            ComPWA::Tools::updateParameter,
        "Update parameters according input FitParameters.", py::arg("tree"),
        py::arg("fit_parameters"));

  // ------- Data

  py::class_<ComPWA::FourMomentum>(m, "FourMomentum")
      .def(py::init<std::array<double, 4>>(),
           "Construct a FourMomentum from a four vector as a list of the form "
           "[px, py, pz, E] and a pid.",
           py::arg("p4"))
      .def("__repr__", [](const ComPWA::FourMomentum &p) {
        std::stringstream ss;
        ss << p;
        return ss.str();
      });

  py::bind_vector<std::vector<ComPWA::FourMomentum>>(m, "FourMomentumList");

  py::class_<ComPWA::Event>(m, "Event")
      .def(py::init<std::vector<ComPWA::FourMomentum>, double>(),
           py::arg("four_momenta"), py::arg("weight") = 1)
      .def_readonly("four_momenta", &ComPWA::Event::FourMomenta)
      .def_readonly("weight", &ComPWA::Event::Weight);

  py::bind_vector<std::vector<ComPWA::Event>>(m, "EventList");

  py::class_<ComPWA::EventCollection>(m, "EventCollection")
      .def(py::init<std::vector<ComPWA::pid>, std::vector<ComPWA::Event>>(),
           py::arg("pids"), py::arg("events"))
      .def_readonly("pids", &ComPWA::EventCollection::Pids)
      .def_readonly("events", &ComPWA::EventCollection::Events)
      .def("to_table",
           [](const ComPWA::EventCollection &self) {
             if (!self.checkPidMatchesEvents())
               throw ComPWA::CorruptFile(
                   "Number of PIDs in EventCollection does not match the "
                   "number of four momenta in each of its events");
             std::vector<std::vector<double>> table;
             for (const auto &Event : self.Events) {
               std::vector<double> row;
               row.reserve(self.Pids.size() * 4);
               for (const auto &Momentum : Event.FourMomenta) {
                 row.push_back(Momentum.px());
                 row.push_back(Momentum.py());
                 row.push_back(Momentum.pz());
                 row.push_back(Momentum.e());
               }
               table.push_back(std::move(row));
             }
             return table;
           })
      .def("weights",
           [](const ComPWA::EventCollection &self) {
             std::vector<double> Weights;
             Weights.reserve(self.Events.size());
             for (const auto &Event : self.Events) {
               Weights.push_back(Event.Weight);
             }
             return Weights;
           })
      .def("has_weights", [](const ComPWA::EventCollection &self) {
        if (!self.Events.size()) {
          return false;
        }
        auto FirstWeight = self.Events.front().Weight;
        for (const auto &Event : self.Events) {
          if (Event.Weight != FirstWeight) {
            return true;
          }
        }
        return false;
      });

  // ------- Data I/O ------- //
  m.def("read_ascii_data", &ComPWA::Data::Ascii::readData,
        "Read ROOT tree from file to an EventList.", py::arg("input_file"),
        py::arg("number_of_events") = -1);
  m.def("write_ascii_data", &ComPWA::Data::Ascii::writeData,
        "Save data as ROOT tree to file.", py::arg("event_list"),
        py::arg("output_file"), py::arg("overwrite") = true);

  m.def("read_root_data", &ComPWA::Data::Root::readData,
        "Read ROOT tree from file to an EventList.", py::arg("input_file"),
        py::arg("tree_name") = "events", py::arg("number_of_events") = -1);
  m.def("write_root_data", &ComPWA::Data::Root::writeData,
        "Save data as ROOT tree to file.", py::arg("event_list"),
        py::arg("output_file"), py::arg("tree_name") = "events",
        py::arg("overwrite") = true);

  py::class_<ComPWA::Data::DataSet>(m, "DataSet")
      .def_readonly("data", &ComPWA::Data::DataSet::Data)
      .def_readonly("weights", &ComPWA::Data::DataSet::Weights)
      .def("has_weights", [](const ComPWA::Data::DataSet &self) {
        if (!self.Weights.size()) {
          return false;
        }
        auto FirstWeight = self.Weights.front();
        for (auto Weight : self.Weights) {
          if (Weight != FirstWeight) {
            return true;
          }
        }
        return false;
      });

  m.def("add_intensity_weights", &ComPWA::Data::addIntensityWeights,
        "Add the intensity values as weights to this data sample.",
        py::arg("intensity"), py::arg("events"), py::arg("kinematics"));

  // ------- Particles
  py::class_<ComPWA::ParticleList>(m, "ParticleList")
      .def(py::init<>())
      .def("__repr__",
           [](const ComPWA::ParticleList &p) {
             std::stringstream ss;
             ss << p;
             return ss.str();
           })
      .def("name_to_pid",
           [](const ComPWA::ParticleList &p, std::string name) {
             return ComPWA::findParticle(p, name).getId();
           },
           "Convert a name to a PID as encoded in this ParticleList object",
           py::arg("name"))
      .def("pid_to_name",
           [](const ComPWA::ParticleList &p, int pid) {
             return ComPWA::findParticle(p, pid).getName();
           },
           "Convert a PID to a name as encoded in this ParticleList object",
           py::arg("pid"));

  m.def("read_particles",
        [](std::string filename) { return ComPWA::readParticles(filename); },
        "Read particles from a xml file.", py::arg("xml_filename"));

  m.def("insert_particles",
        [](ComPWA::ParticleList &partlist, std::string filename) {
          ComPWA::insertParticles(partlist, filename);
        },
        "Insert particles to a list from a xml file. Already defined particles "
        "will be overwritten!");

  // ------- Kinematics

  py::class_<ComPWA::Kinematics, std::shared_ptr<ComPWA::Kinematics>>(
      m, "Kinematics")
      .def("convert", &ComPWA::Kinematics::convert,
           "Convert an `.EventCollection` to a `.DataSet`.")
      .def("phsp_volume", &ComPWA::Kinematics::phspVolume,
           "Get phase space volume defined by the kinematics.");

  py::class_<ComPWA::Physics::ParticleStateTransitionKinematicsInfo>(
      m, "ParticleStateTransitionKinematicsInfo")
      .def("get_final_state_id_to_name_mapping",
           &ComPWA::Physics::ParticleStateTransitionKinematicsInfo::
               getFinalStateIDToNameMapping,
           "Get a dictionary for converting a final state ID to a name");

  py::class_<
      ComPWA::Physics::HelicityFormalism::HelicityKinematics,
      ComPWA::Kinematics,
      std::shared_ptr<ComPWA::Physics::HelicityFormalism::HelicityKinematics>>(
      m, "HelicityKinematics")
      .def(py::init<ComPWA::ParticleList, std::vector<ComPWA::pid>,
                    std::vector<ComPWA::pid>, std::array<double, 4>>())
      .def(py::init<ComPWA::ParticleList, std::vector<ComPWA::pid>,
                    std::vector<ComPWA::pid>>())
      .def(py::init<
           const ComPWA::Physics::ParticleStateTransitionKinematicsInfo &,
           double>())
      .def(py::init<
           const ComPWA::Physics::ParticleStateTransitionKinematicsInfo &>())
      .def("convert",
           py::overload_cast<const ComPWA::EventCollection &>(
               &ComPWA::Physics::HelicityFormalism::HelicityKinematics::convert,
               py::const_),
           py::arg("Event"))
      .def("create_all_subsystems", &ComPWA::Physics::HelicityFormalism::
                                        HelicityKinematics::createAllSubsystems)
      .def("get_particle_state_transition_kinematics_info",
           &ComPWA::Physics::HelicityFormalism::HelicityKinematics::
               getParticleStateTransitionKinematicsInfo);

  m.def("create_helicity_kinematics",
        [&](const std::string &XmlFile, ComPWA::ParticleList ParticleList) {
          return ComPWA::Physics::createHelicityKinematics(ParticleList,
                                                           XmlFile);
        },
        "Create a helicity kinematics object from an XML file. The file should "
        "contain a kinematics section.",
        py::arg("xml_filename"), py::arg("particle_list"));

  m.def(
      "create_helicity_kinematics",
      [&](const std::string &XmlFile) {
        return ComPWA::Physics::createHelicityKinematics(XmlFile);
      },
      "Create a helicity kinematics object from an XML file. The file should "
      "contain a kinematics section **and a particle section**.",
      py::arg("xml_filename"));

  m.def(
      "compute_kinematic_variables",
      [&](const ComPWA::EventCollection &Events, const std::string &XmlFile) {
        auto Kinematics = ComPWA::Physics::createHelicityKinematics(XmlFile);
        Kinematics.createAllSubsystems();
        return Kinematics.convert(Events);
      },
      "Directly convert an `.EventCollection` to a `.DataSet` using a model "
      "file. A Kinematics object is created from the XML file, so this is a "
      "façade to the `.HelicityKinematics` class.",
      py::arg("event_collection"), py::arg("xml_filename"));

  m.def(
      "get_final_state_id_to_name_mapping",
      [&](const std::string &XmlFile) {
        auto Kinematics = ComPWA::Physics::createHelicityKinematics(XmlFile);
        auto TransInfo = Kinematics.getParticleStateTransitionKinematicsInfo();
        return TransInfo.getFinalStateIDToNameMapping();
      },
      "Directly get a final state ID to particle name mapping from an XML "
      "file.",
      py::arg("xml_filename"));

  // ------- Intensity

  py::class_<ComPWA::Intensity, std::shared_ptr<ComPWA::Intensity>>(
      m, "Intensity");

  py::class_<ComPWA::FunctionTree::FunctionTreeIntensity, ComPWA::Intensity,
             std::shared_ptr<ComPWA::FunctionTree::FunctionTreeIntensity>>(
      m, "FunctionTreeIntensity")
      .def("evaluate", &ComPWA::FunctionTree::FunctionTreeIntensity::evaluate)
      .def("updateParametersFrom",
           [](ComPWA::FunctionTree::FunctionTreeIntensity &x,
              ComPWA::FitParameterList pars) {
             std::vector<double> params;
             for (auto x : pars)
               params.push_back(x.Value);
             x.updateParametersFrom(params);
           })
      .def("print", &ComPWA::FunctionTree::FunctionTreeIntensity::print,
           "print function tree");

  py::class_<ComPWA::Tools::IntensityComponent>(m, "IntensityComponent");

  py::class_<ComPWA::Physics::IntensityBuilderXML>(m, "IntensityBuilderXML")
      .def(
          py::init([](const std::string &filename, ComPWA::ParticleList partL,
                      ComPWA::Kinematics &kin,
                      const ComPWA::EventCollection &PhspSample) {
            boost::property_tree::ptree pt;
            boost::property_tree::xml_parser::read_xml(filename, pt);
            auto it = pt.find("Intensity");
            if (it != pt.not_found()) {
              ComPWA::Physics::IntensityBuilderXML Builder(
                  partL, kin, it->second, PhspSample);
              return Builder;
            } else {
              throw ComPWA::BadConfig("pycompwa::IntensityBuilderXML(): "
                                      "Intensity tag not found in xml file!");
            }
          }),
          "Create an intensity and a helicity kinematics from a xml file. The "
          "file should contain a particle list, and a kinematics and intensity "
          "section.",
          py::arg("xml_filename"), py::arg("particle_list"),
          py::arg("kinematics"), py::arg("phsp_sample"))
      .def("create_intensity",
           &ComPWA::Physics::IntensityBuilderXML::createIntensity)
      .def("create_intensity_components",
           &ComPWA::Physics::IntensityBuilderXML::createIntensityComponents,
           py::arg("component_name_lists"))
      .def("get_all_component_names",
           &ComPWA::Physics::IntensityBuilderXML::getAllComponentNames);

  //------- Generate

  py::class_<ComPWA::UniformRealNumberGenerator>(m,
                                                 "UniformRealNumberGenerator");

  py::class_<ComPWA::StdUniformRealGenerator,
             ComPWA::UniformRealNumberGenerator>(m, "StdUniformRealGenerator")
      .def(py::init<int>());

  py::class_<ComPWA::Data::Root::RootUniformRealGenerator,
             ComPWA::UniformRealNumberGenerator>(m, "RootUniformRealGenerator")
      .def(py::init<int>());

  py::class_<ComPWA::PhaseSpaceEventGenerator>(m, "PhaseSpaceEventGenerator");

  py::class_<ComPWA::Data::Root::RootGenerator,
             ComPWA::PhaseSpaceEventGenerator>(m, "RootGenerator")
      .def(py::init<
           const ComPWA::Physics::ParticleStateTransitionKinematicsInfo &>());

  py::class_<ComPWA::Data::EvtGen::EvtGenGenerator,
             ComPWA::PhaseSpaceEventGenerator>(m, "EvtGenGenerator")
      .def(py::init<
           const ComPWA::Physics::ParticleStateTransitionKinematicsInfo &>());

  m.def("generate",
        [](unsigned int NumberOfEvents,
           std::shared_ptr<ComPWA::Kinematics> Kinematics,
           const ComPWA::PhaseSpaceEventGenerator &Generator,
           std::shared_ptr<ComPWA::Intensity> Intensity,
           ComPWA::UniformRealNumberGenerator &RandomGenerator) {
          return ComPWA::Data::generate(NumberOfEvents, *Kinematics, Generator,
                                        *Intensity, RandomGenerator);
        },
        "Generate sample from an Intensity", py::arg("size"),
        py::arg("kinematics"), py::arg("phsp_generator"), py::arg("intensity"),
        py::arg("random_generator"));

  m.def("generate",
        [](unsigned int NumberOfEvents,
           std::shared_ptr<ComPWA::Kinematics> Kinematics,
           ComPWA::UniformRealNumberGenerator &RandomGenerator,
           std::shared_ptr<ComPWA::Intensity> Intensity,
           const ComPWA::EventCollection &PhspSample) {
          return ComPWA::Data::generate(NumberOfEvents, *Kinematics,
                                        RandomGenerator, *Intensity,
                                        PhspSample);
        },
        "Generate sample from an Intensity, using a given phase space sample.",
        py::arg("size"), py::arg("kinematics"), py::arg("generator"),
        py::arg("intensity"), py::arg("phsp_sample"));

  m.def("generate",
        [](unsigned int NumberOfEvents,
           std::shared_ptr<ComPWA::Kinematics> Kinematics,
           ComPWA::UniformRealNumberGenerator &RandomGenerator,
           std::shared_ptr<ComPWA::Intensity> Intensity,
           const ComPWA::EventCollection &PhspSample,
           const ComPWA::EventCollection &ToyPhspSample) {
          return ComPWA::Data::generate(NumberOfEvents, *Kinematics,
                                        RandomGenerator, *Intensity, PhspSample,
                                        ToyPhspSample);
        },
        "Generate sample from an Intensity. In case that detector "
        "reconstruction and selection is considered in the phase space sample "
        "a second pure toy sample needs to be passed.",
        py::arg("size"), py::arg("kinematics"), py::arg("generator"),
        py::arg("intensity"), py::arg("phsp_sample"),
        py::arg("toy_phsp_sample") = nullptr);

  m.def("generate_phsp", &ComPWA::Data::generatePhsp,
        "Generate phase space sample");

  m.def("generate_importance_sampled_phsp",
        &ComPWA::Data::generateImportanceSampledPhsp,
        "Generate an Intensity importance weighted phase space sample",
        py::arg("size"), py::arg("kinematics"), py::arg("generator"),
        py::arg("intensity"), py::arg("random_generator"));

  //------- Estimator + Optimizer

  py::class_<ComPWA::Estimator::Estimator<double>>(m, "Estimator");

  py::class_<ComPWA::FunctionTree::FunctionTreeEstimator,
             ComPWA::Estimator::Estimator<double>>(m, "FunctionTreeEstimator")
      .def("print", &ComPWA::FunctionTree::FunctionTreeEstimator::print,
           "print function tree");

  m.def("create_unbinned_log_likelihood_function_tree_estimator",
        (std::pair<ComPWA::FunctionTree::FunctionTreeEstimator,
                   ComPWA::FitParameterList>(*)(
            ComPWA::FunctionTree::FunctionTreeIntensity &,
            const ComPWA::Data::DataSet &)) &
            ComPWA::Estimator::createMinLogLHFunctionTreeEstimator,
        py::arg("intensity"), py::arg("datapoints"));

  py::class_<
      ComPWA::Optimizer::Optimizer<ComPWA::Optimizer::Minuit2::MinuitResult>>(
      m, "Optimizer");

  py::class_<
      ComPWA::Optimizer::Minuit2::MinuitIF,
      ComPWA::Optimizer::Optimizer<ComPWA::Optimizer::Minuit2::MinuitResult>>(
      m, "MinuitIF")
      .def(py::init<>())
      .def("optimize", &ComPWA::Optimizer::Minuit2::MinuitIF::optimize,
           "Start minimization.");

  //------- FitResult

  py::class_<ComPWA::FitResult>(m, "FitResult")
      .def_readonly("final_parameters", &ComPWA::FitResult::FinalParameters)
      .def_readonly("initial_parameters", &ComPWA::FitResult::InitialParameters)
      .def_readonly("initial_estimator_value",
                    &ComPWA::FitResult::InitialEstimatorValue)
      .def_readonly("final_estimator_value",
                    &ComPWA::FitResult::FinalEstimatorValue)
      .def_property_readonly(
          "fit_duration_in_seconds",
          [](const ComPWA::FitResult &x) { return x.FitDuration.count(); })
      .def_readonly("covariance_matrix", &ComPWA::FitResult::CovarianceMatrix)
      .def("write", &ComPWA::FitResult::write,
           "Write fit result to an xml file.", py::arg("filename"));

  m.def("load", &ComPWA::Optimizer::Minuit2::load,
        "Load a Minuit2 fit result from a file.", py::arg("filename"));

  m.def("load", &ComPWA::load, "Load a fit result from a file.",
        py::arg("filename"));

  py::class_<ComPWA::Optimizer::Minuit2::MinuitResult, ComPWA::FitResult>(
      m, "MinuitResult")
      .def("log",
           [](const ComPWA::Optimizer::Minuit2::MinuitResult &Result) {
             LOG(INFO) << Result;
           },
           "Print fit result to the logging system.")
      .def("write", &ComPWA::Optimizer::Minuit2::MinuitResult::write,
           "Write Minuit2 fit result to an xml file.", py::arg("filename"));

  m.def("initializeWithFitResult", &ComPWA::initializeWithFitResult,
        "Initializes an Intensity with the parameters of a FitResult.",
        py::arg("intensity"), py::arg("fit_result"));

  py::class_<ComPWA::Tools::FitFraction>(m, "FitFraction")
      .def("__repr__",
           [](const ComPWA::Tools::FitFraction &FF) {
             std::stringstream ss;
             ss << FF.Name << ": " << FF.Value << " +- " << FF.Error << "\n";
             return ss.str();
           })
      .def_readonly("name", &ComPWA::Tools::FitFraction::Name)
      .def_readonly("value", &ComPWA::Tools::FitFraction::Value)
      .def_readonly("error", &ComPWA::Tools::FitFraction::Error);

  m.def("fit_fractions_with_propagated_errors",
        [](const std::vector<std::pair<ComPWA::Tools::IntensityComponent,
                                       ComPWA::Tools::IntensityComponent>>
               &Components,
           const ComPWA::Data::DataSet &PhspSample,
           const ComPWA::FitResult &Result) {
          ComPWA::Tools::FitFractions FF;
          return FF.calculateFitFractionsWithCovarianceErrorPropagation(
              Components, PhspSample, Result);
        },
        "Calculates the fit fractions and errors for all given components.",
        py::arg("intensity_components"), py::arg("sample"),
        py::arg("fit_result"));

  //------- Plotting

  m.def("create_data_array",
        [](ComPWA::Data::DataSet DataSample) {
          std::vector<std::string> KinVarNames;
          std::vector<std::vector<double>> DataArray;
          for (auto const &x : DataSample.Data) {
            KinVarNames.push_back(x.first);
            DataArray.push_back(x.second);
          }
          KinVarNames.push_back("weight");
          DataArray.push_back(DataSample.Weights);
          return std::make_pair(KinVarNames, DataArray);
        },
        py::return_value_policy::move);

  m.def("create_fitresult_array",
        [](std::shared_ptr<ComPWA::Intensity> Intensity,
           ComPWA::Data::DataSet DataSample) {
          std::vector<std::string> KinVarNames;
          std::vector<std::vector<double>> DataArray;
          for (auto const &x : DataSample.Data) {
            KinVarNames.push_back(x.first);
            DataArray.push_back(x.second);
          }
          KinVarNames.push_back("intensity");
          KinVarNames.push_back("weight");

          DataArray.push_back(DataSample.Weights);
          DataArray.push_back(Intensity->evaluate(DataSample.Data));
          return std::make_pair(KinVarNames, DataArray);
        },
        py::return_value_policy::move);

  m.def(
      "create_rootplotdata",
      [](const std::string &filename, std::shared_ptr<ComPWA::Kinematics> kin,
         const ComPWA::Data::DataSet &DataSample,
         const ComPWA::Data::DataSet &PhspSample,
         std::shared_ptr<ComPWA::Intensity> Intensity,
         std::map<std::string, std::shared_ptr<ComPWA::Intensity>>
             IntensityComponents,
         const ComPWA::Data::DataSet &HitAndMissSample,
         const std::string &option) {
        try {
          auto KinematicsInfo =
              (std::dynamic_pointer_cast<
                   ComPWA::Physics::HelicityFormalism::HelicityKinematics>(kin)
                   ->getParticleStateTransitionKinematicsInfo());
          ComPWA::Tools::Plotting::RootPlotData plotdata(KinematicsInfo,
                                                         filename, option);
          plotdata.writeData(DataSample);
          if (Intensity) {
            plotdata.writeIntensityWeightedPhspSample(
                PhspSample, *Intensity,
                std::string("intensity_weighted_phspdata"),
                IntensityComponents);
          }
          plotdata.writeHitMissSample(HitAndMissSample);
        } catch (const std::exception &e) {
          LOG(ERROR) << e.what();
        }
      },
      py::arg("filename"), py::arg("kinematics"), py::arg("data_sample"),
      py::arg("phsp_sample") = ComPWA::Data::DataSet(),
      py::arg("intensity") = std::shared_ptr<ComPWA::Intensity>(nullptr),
      py::arg("intensity_components") =
          std::map<std::string, std::shared_ptr<ComPWA::Intensity>>(),
      py::arg("hit_and_miss_sample") = ComPWA::Data::DataSet(),
      py::arg("tfile_option") = "RECREATE");
}
