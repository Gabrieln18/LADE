agent: geospatial-engineer
skills:
  - geospatial/raster-processing
  - geospatial/vector-processing
  - geospatial/crs
  - geospatial/earth-observation
  - geospatial/spatiotemporal
  - processing/dask-xarray
  - processing/apache-sedona
references:        # on demand, via agents/geospatial-engineer/references/index.md
  - references/lattinus.md
  - references/domain/earth-observation.md
  - references/domain/geospatial.md
  - references/domain/agriculture.md
  - references/platform/jaguar.md
  - references/platform/mirage.md
  - references/lattinus-code.md        # §8 only
  - references/engineering/python.md
  - references/engineering/data.md
policies: [safety, dependencies, git, documentation]
workflows: [feature-development, bug-investigation, new-module]
can_write:         # subset of permissions.md §4/§5; paths declared in task.md
  - geospatial processing artifacts (raster/vector, CRS, EO, Dask/Xarray, Sedona)
  - memory/open-questions.md (append-only)