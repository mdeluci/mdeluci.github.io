---
layout: post
title: Phase-field Modeling of Dendritic Solidification
date: 2024-06-20 02:52:00-0400
description: we solve a phase-field model of dendritic soldification with surface tension anisotropy by means of isogeometric analysis.
tags: Phase-field PDEs IGA
categories: Projects
thumbnail: assets/img/sol_1.jpg
related_posts: false
---

## Phase-field equation for solidification processes
The Cahn–Hilliard equation describes the process of phase separation, by which the two components of a binary fluid spontaneously separate and form domains pure in each component. It was originally proposed in 1958 to model phase separation in binary alloys {% cite Cahn-Hilliard Cahn-Hilliard2 --collection external_references %}. Since then it has been used to describe various phenomena, such as spinodal decomposition {% cite MARALDI201231 --collection external_references %}, diblock copolymer {% cite Choksi --collection external_references %}, image inpainting {% cite 4032803 --collection external_references %}, tumor growth simulation {% cite tumor --collection external_references %} or multiphase fluid flows {% cite BADALASSI2003371 --collection external_references %}.

<div class="container">
    <div class="row justify-content-center mt-3">
        <div class="col mt-3 mt-md-0 d-flex justify-content-center">
            <div style="width: 90%;"> <!-- Container div to control width -->
                {% include video.liquid path="assets/video/solidification.mp4" class="img-fluid rounded z-depth-1" controls=true autoplay=true %}
            </div>
        </div>
    </div>
    <div class="caption text-center">
          Crystal growth from a square-shaped seed located in an undercooled region. Phase-field (top row). Temperature (bottom row)
    </div>
</div>

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/sol_1.jpg" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/sol_2.jpg" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Crystal growth from a square-shaped seed located in an undercooled region. Here we show the time evolution of dendritic solidification for different mode numbers of anisotropy. Time evolution of the temperature field from the initial square-shaped seed for different mode numbers of anisotropy.
</div>
