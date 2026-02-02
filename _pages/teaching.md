---
layout: page
permalink: /teaching/
title: Teaching
description:
nav: true
nav_order: 8
tikzjax: true
---

My teaching philosophy and interests are described in the diagrams below (they take a few seconds to show. Be patient)  

<!-- First Diagram -->
<div class="tikzjax">
\begin{tikzpicture}[
    node distance=3cm and 4cm,
    every node/.style={draw, rectangle, rounded corners, align=center},
    main/.style={draw, rectangle, rounded corners, fill=blue!20, text width=4cm},
    sub/.style={draw, rectangle, rounded corners, fill=green!20, text width=4cm},
    connect/.style={-latex, thick, orange}
]

\node[main] (philosophy) {Teaching Philosophy:\\ Hybrid Project-Based Model};

\node[sub, below left=of philosophy] (exams) {Conventional Examinations};
\node[sub, below=of philosophy] (projects) {Hands-on Projects};
\node[sub, below right=of philosophy] (skills) {Skill Development};

\node[sub, below=of projects] (practical) {Real-World Applications};
\node[sub, below=of practical] (curiosity) {Curiosity \& Ownership};
\node[sub, below=of curiosity] (teamwork) {Problem-solving \& Teamwork};

\node[sub, below=of skills] (workshops) {Workshops/Training};
\node[sub, below=of workshops] (interdisciplinary) {Interdisciplinary Cooperation};
\node[sub, below=of interdisciplinary] (industry) {Industry Partnerships};
\node[sub, below=of industry] (supportive) {Supportive Atmosphere};

\draw[connect] (philosophy) -- (exams);
\draw[connect] (philosophy) -- (projects);
\draw[connect] (philosophy) -- (skills);

\draw[connect] (projects) -- (practical);
\draw[connect] (practical) -- (curiosity);
\draw[connect] (curiosity) -- (teamwork);

\draw[connect] (skills) -- (workshops);
\draw[connect] (workshops) -- (interdisciplinary);
\draw[connect] (interdisciplinary) -- (industry);
\draw[connect] (industry) -- (supportive);

\end{tikzpicture>
</div>

<!-- Second Diagram -->
<div class="tikzjax">
\begin{tikzpicture}[
    node distance=2cm,
    every node/.style={draw, rectangle, rounded corners, align=center},
    main/.style={draw, rectangle, rounded corners, fill=blue!20, text width=3cm},
    sub/.style={draw, rectangle, rounded corners, fill=green!20, text width=3cm},
    course/.style={draw, rectangle, rounded corners, fill=yellow!20, text width=3cm},
    connect/.style={-latex, thick, orange}
]

\node[main] (focus) {Teaching Focus:\\ Practical Impact of Computational Modeling};

\node[sub, below left=of focus] (fundamentals) {Fundamental Principles};
\node[sub, below right=of focus] (advanced) {Advanced Methodologies};
\node[sub, below=of focus] (courses) {Courses};

\node[course, below=1.5cm of fundamentals] (solid) {Solid Mechanics};
\node[course, below=of solid] (fluid) {Fluid Mechanics};
\node[course, below=of fluid] (fea) {Intro to Finite Element Analysis};
\node[course, below=of fea] (cfd) {Intro to Computational Fluid Dynamics};

\node[course, below=1.5cm of advanced] (biomed) {Computational Modeling in Biomedical Engineering};
\node[course, below=of biomed] (nonlinear) {Nonlinear Finite Element Methods};
\node[course, below=of nonlinear] (porous) {Transport Processes in Porous Media};
\node[course, below=of porous] (advancedcfd) {Advanced Computational Fluid Dynamics};

\node[sub, below=1.5cm of courses] (newcourses) {Development of New Courses};

\draw[connect] (focus) -- (fundamentals);
\draw[connect] (focus) -- (advanced);
\draw[connect] (focus) -- (courses);

\draw[connect] (fundamentals) -- (solid);
\draw[connect] (solid) -- (fluid);
\draw[connect] (fluid) -- (fea);
\draw[connect] (fea) -- (cfd);

\draw[connect] (advanced) -- (biomed);
\draw[connect] (biomed) -- (nonlinear);
\draw[connect] (nonlinear) -- (porous);
\draw[connect] (porous) -- (advancedcfd);

\draw[connect] (courses) -- (newcourses);

\end{tikzpicture>
</div>
