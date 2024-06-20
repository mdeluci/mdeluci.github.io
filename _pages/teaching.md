---
layout: page
permalink: /teaching/
title: Teaching
description: Materials for courses you taught. Replace this text with your description.
nav: true
nav_order: 8
tikzjax: true
---

For now, this page is assumed to be a static description of your courses. You can convert it to a collection similar to `_projects/` so that you can have a dedicated page for each course.

Organize your courses by years, topics, or universities, however you like!

<div class="container">
    <div class="row justify-content-center mt-3">
        <div class="col mt-3 mt-md-0 d-flex justify-content-center">
            <div style="width: 80%;"> <!-- Container div to control width -->
                {% include figure.liquid loading="eager" path="assets/img/Diagram1_teaching.jpg" class="img-fluid rounded z-depth-1" %}
            </div>
        </div>
    </div>
    <div class="caption text-center">
        Teaching philosophy.
    </div>
</div>

<script type="text/tikz">
\begin{tikzpicture}[
    node distance=2cm,
    every node/.style={draw, rectangle, rounded corners, align=center},
    main/.style={draw, rectangle, rounded corners, fill=blue!20, text width=3cm},
    sub/.style={draw, rectangle, rounded corners, fill=green!20, text width=3cm},
    course/.style={draw, rectangle, rounded corners, fill=yellow!20, text width=3cm},
    connect/.style={-latex, thick}
    ]

% Central node
\node[main] (focus) {Teaching Focus:\\ Practical Impact of Computational Modeling};

% First layer of nodes
\node[sub, below left=of focus] (fundamentals) {Fundamental Principles};
\node[sub, below right=of focus] (advanced) {Advanced Methodologies};
\node[sub, below=of focus] (courses) {Courses};

% Second layer of nodes under 'Fundamentals'
\node[course, below=1.5cm of fundamentals] (solid) {Solid Mechanics};
\node[course, below=of solid] (fluid) {Fluid Mechanics};
\node[course, below=of fluid] (fea) {Intro to Finite Element Analysis};
\node[course, below=of fea] (cfd) {Intro to Computational Fluid Dynamics};

% Second layer of nodes under 'Advanced'
\node[course, below=1.5cm of advanced] (biomed) {Computational Modeling in Biomedical Engineering};
\node[course, below=of biomed] (nonlinear) {Nonlinear Finite Element Methods};
\node[course, below=of nonlinear] (porous) {Transport Processes in Porous Media};
\node[course, below=of porous] (advancedcfd) {Advanced Computational Fluid Dynamics};

% Second layer of nodes under 'Courses'
\node[sub, below=1.5cm of courses] (newcourses) {Development of New Courses};

% Connections from central node to first layer
\draw[connect] (focus) -- (fundamentals);
\draw[connect] (focus) -- (advanced);
\draw[connect] (focus) -- (courses);

% Connections from 'Fundamentals' to its courses
\draw[connect] (fundamentals) -- (solid);
\draw[connect] (solid) -- (fluid);
\draw[connect] (fluid) -- (fea);
\draw[connect] (fea) -- (cfd);

% Connections from 'Advanced' to its courses
\draw[connect] (advanced) -- (biomed);
\draw[connect] (biomed) -- (nonlinear);
\draw[connect] (nonlinear) -- (porous);
\draw[connect] (porous) -- (advancedcfd);

% Connection from 'Courses' to 'New Courses'
\draw[connect] (courses) -- (newcourses);

\end{tikzpicture}
</script>
