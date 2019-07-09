---
title: 'drms: A Python package for accessing HMI and AIA data'
tags:
  - Python
  - astronomy
authors:
  - name: Kolja Glogowski
    orcid: 0000-0002-1361-5712
    affiliation: "1, 2"
  - name: Monica G. Bobra
    orcid: 0000-0002-5662-9604
    affiliation: 3
  - name: Nitin Choudhary
    orcid: 0000-0001-6915-4583
    affiliation: 4
  - name: Arthur B. Amezcua
    orcid:
    affiliation: 3
  - name: Stuart J. Mumford
    orcid: 0000-0003-4217-4642
    affiliation: 5
affiliations:
 - name: Kiepenheuer Institut für Sonnenphysik, 79104, Freiburg, Germany
   index: 1
 - name: eScience Department, Computing Center, University of Freiburg, 79104, Freiburg, Germany
   index: 2
 - name: W.W. Hansen Experimental Physics Laboratory, Stanford University, Stanford, CA 94305, USA
   index: 3
 - name: Department of Mathematics, Indian Institute of Technology Kharagpur, Kharagpur, West Bengal 721302, India
   index: 4
 - name: School of Mathematics and Statistics, The University of Sheffield, Sheffield S3 7RH, UK
   index: 5
date: 02 July 2019
bibliography: paper.bib
---

# Summary

The NASA Solar Dynamics Observatory (SDO) spacecraft has continuously observed the Sun since 2010. It takes about 1.5 terabytes of data per day, in the form of images or spectral data and associated metadata. The data from two of its instruments, Helioseismic and Magnetic Imager [HMI; @schou12] and Atmospheric Imaging Assembly (AIA) [AIA; @lemen12], are stored and distributed by the Joint Science Operations Center (JSOC) at Stanford University. Specifically, the metadata and pointers to the image data are stored in a PostgreSQL database and managed by the Data Record Management System (DRMS). The data and metadata can be accessed using the [JSOC website](http://jsoc.stanford.edu/ajax/lookdata.html).

`drms` is a SunPy-affiliated [@SunPy2015] Python package for accessing data hosted by JSOC. A vast majority of these data come from the HMI and AIA instruments, but JSOC also hosts data from the Michelson Doppler Imager [MDI; @Scherrer1995] aboard the Solar and Heliospheric Observatory (SOHO) spacecraft and data from the Interface Region Imaging Spectrometer [IRIS; @DePontieu2014]. The `drms` package allows users to execute complex queries across any number of metadata keywords and export tailored datasets in a variety of formats (including FITS files, movies, and images).

The `drms` package is used as backend for SunPy's JSOC client, but it can also be installed independently from [PyPI](https://pypi.org/project/drms/) using `pip` or from [`conda-forge`](https://anaconda.org/conda-forge/drms) using the `conda` package manager. Source code and documentation are available on [GitHub](https://github.com/sunpy/drms) and the [SunPy website](https://docs.sunpy.org/projects/drms/en/latest) respectively. The `drms` client communicates with DRMS servers over HTTP using a REST API. By default the `drms` client connects to the JSOC DRMS, but it can also be configured to access local DRMS installations at other sites, provided the site runs a webserver hosting the required CGIs.

One advantage of the DRMS is that it decouples metadata from image data. This means that a user can access and export metadata without downloading any image data. Users can also construct queries across any number of metadata keywords, to only download images of interest.

Each data collection in JSOC (for example, AIA images of the solar corona in 171 Å or HMI maps of the photospheric magnetic field in 6173 Å) is associated with its own database table and called a *data series*. An example of a data series with rich, valuable metadata is called `hmi.sharp_720s` and contains Space-weather HMI Active Region Patches [@Bobra14], or SHARPs.

![Left: Total unsigned flux and mean current helicity of HMI Active Region Patch (HARP) Number 4315 during its disk passage; the dashed orange line marks the central meridian crossing of the active region. Right: Continuum intensity map and magnetic field map at the time of the central meridian crossing.](sharp.pdf)

The left two panels of Figure 1 show a small selection of the available metadata which characterize a particular solar active region. From the steep gradient in the total unsigned magnetic flux and the increasing area of active pixels, it is directly evident, without inspecting any image data, that this is a strong emerging active region. The right two panels show a selection of image data corresponding to the time indicated by the dashed orange line in the left two panels. Figure 1 was created from metadata and image data obtained from the JSOC DRMS server using the `drms` package.


# Acknowledgements

The data used here are courtesy of the GOES team and the Helioseismic and Magnetic Imager (HMI) and Atmospheric Imaging Assembly (AIA) science teams of the NASA Solar Dynamics Observatory. The development of this software was partially supported by the European Research Council under the European Union's Seventh Framework Programme (FP/2007-2013) / ERC Grant Agreement no. 307117 and by NASA Grant NAS5-02139 (HMI).

# References
