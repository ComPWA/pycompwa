.. _python-ui:

Python UI
---------

The Python User Interface is a python module named :code:`ui`, built with 
`pybind11 <https://pybind11.readthedocs.io/en/stable/index.html>`_.
It is the recommended way to use ComPWA, since the user benefits from the python
ease of use.

.. note::
   Because the Python UI calls the c++ code in the background, you do not have 
   to worry about speed. It runs just as fast ;)

Since the Python UI just binds to the c++ user interface code, there is a strong
correlation between the two. It's useful to read more about the
`ComPWA modules <https://compwa.github.io/ComPWA>`_.

.. hint::
   On how to use the Python UI, also refer to the
   :ref:`examples section<examples>`.

The Python UI enables you to perform all of the tasks needed for your partial 
wave analysis: 

.. _dataio:

Read and Write Data Samples
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Currently only the reading and writing of ROOT files is supported via the
:class:`.RootDataIO` class.

.. autoclass:: pycompwa.ui.RootDataIO
   :members:
   :noindex:

For the reading of data/events a predefined tree structure is assumed. The name
of the tree inside the file and the number of events to process can be by 
adjusted in the constructor. By default the tree name is *"data"* and all events
are processed. Inside the tree a :cpp:class:`TClonesArray` with the name 
*"Particles"* is expected. This :cpp:class:`TClonesArray` should contain 
:cpp:class:`TParticle`'s, the final state particles.

The order of the particles inside the :cpp:class:`TClonesArray` can easily be
adjusted in the Kinematics section of your model xml file. Just use the 
``PositionIndex`` attribute to specify the position inside the 
:cpp:class:`TClonesArray`.

Generate Data Samples
^^^^^^^^^^^^^^^^^^^^^

With :mod:`pycompwa.ui` you can also easily create various types of Monte Carlo
data samples:

.. _generatephsp:

* Generating phase space samples based on the Kinematics

  .. autofunction:: pycompwa.ui.generate_phsp
     :noindex:

  A required argument is a :class:`PhaseSpaceGenerator` instance. There are
  currently two options: :class:`.EvtGenGenerator` and :class:`.RootGenerator`.
  Using the :class:`.EvtGenGenerator` is recommended, due to numerical precision
  reasons.

  .. autoclass:: pycompwa.ui.EvtGenGenerator
   :special-members: __init__
   :noindex:

  To initialize such a PhaseSpaceGenerator the Kinematics information of the
  reaction is required. This can be extracted from the 
  :class:`.HelicityKinematics`.
  Read :ref:`below<create-kin-and-intens>` on how to create such a Kinematics
  instance.

  The second argument for the :func:`.generate_phsp` function is a random number
  generator. Here also two options exist:

  *  .. autoclass:: pycompwa.ui.StdUniformRealGenerator
        :special-members: __init__
        :noindex:
  *  .. autoclass:: pycompwa.ui.RootUniformRealGenerator
        :special-members: __init__
        :noindex:
  
* Generating data samples based on a Intensity

  The usage is similar to the :ref:`phase space generation<generatephsp>`. Now
  the Intensity has to be given as an additional argument. A hit-or-miss based
  sampling will be performed. 

  .. autofunction:: pycompwa.ui.generate
     :noindex:

* Generating an importance weighted phase space sample

  .. autofunction:: pycompwa.ui.generate_importance_sampled_phsp
     :noindex:

  .. warning::
     The current implementation is simple and uniformly generates events in the
     phase space domain. Depending on the shape of your Intensity, this can be
     quite computation intensive. However, ideally you would only run this once
     for a specific reaction. 

.. _loadparticles:

Loading and Defining Particles
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Particles can loaded and stored inside a :class:`.PartList`. 

.. autofunction:: pycompwa.ui.read_particles

Also particles can be inserted to an existing :class:`.PartList`, overwriting
already existing particles.

.. autofunction:: pycompwa.ui.insert_particles

.. _create-kin-and-intens:

Create a Kinematics and Intensity Instance from a Description
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As a prerequisite a :class:`.PartList` has to be already loaded.

A HelicityKinematics instance can be created with 
:func:`.create_helicity_kinematics`

.. autofunction:: pycompwa.ui.create_helicity_kinematics
   :noindex:

Analogous a Intensity instance can be created with :func:`.create_intensity`

.. autofunction:: pycompwa.ui.create_intensity
   :noindex:

Here the order of execution is important and can be slightly confusing.
In order to fit an Intensity to a data sample, the Intensity has to be
normalized (when using an unbinned log likelihood estimator). Because the
normalization is performed by MC integration, a phase space sample is needed.
This however requires a Kinematics instance. Therefore the order of execution is:

1. Create/Load a :class:`.PartList`
2. Create a Kinematics instance
3. Create a phase space sample (alternatively: the data can also be 
   :ref:`read from file<dataio>`)
4. Create an Intensity using the phase space sample and the Kinematics instance

   
Fit an Intensity to a Data Sample
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Coming soon...

Save a Fit Result
^^^^^^^^^^^^^^^^^

Coming soon...

Load and Initialize a previous Fit Result
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Coming soon...

Visualizing of data samples and Intensities can be done via the 
:mod:`pycompwa.plotting module` documented in the next section.

