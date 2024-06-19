---
layout: post
title: Solving the Cahn-Hilliard equation on complex geometries
date: 2024-06-19 02:52:00-0400
description: We solve the Cahn-Hilliard equation on a quarter of annulus by means of isogeometric analysis. We adopt the split form of the equation to avoid introducing fourth-order operators and facilitate the imposition of the boundary conditions on the circular geometry,
tags: Cahn-Hilliard PDEs IGA
categories: Projects
related_posts: false
---

## The Cahn-Hilliard equation
The Cahn–Hilliard equation describes the process of phase separation, by which the two components of a binary fluid spontaneously separate and form domains pure in each component. It was originally proposed in 1958 to model phase separation in binary alloys \cite{Cahn-Hilliard, Cahn-Hilliard2}. Since then it has been used to describe various phenomena, such as spinodal decomposition \cite{MARALDI201231}, diblock copolymer \cite{Choksi,JEONG20141263}, image inpainting \cite{4032803}, tumor growth simulation \cite{tumor,WISE2008524} or multiphase fluid flows \cite{BADALASSI2003371, Kotschote}. 

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include video.liquid path="assets/video/ch.mp4" class="img-fluid rounded z-depth-1" controls=true autoplay=true %}
    </div>
</div>
<div class="caption">
    Solution of the Cahn-Hilliard equation on a quarter of anulus from a randomly perturbed initial condition.
</div>

There are two main approaches to describing phase transition phenomena: sharp-interface models and phase-field models. Sharp-interface models involve the resolution of a moving boundary problem, meaning that partial differential equations have to be solved for each phase. This can lead to physical \cite{Anderson} and computational complications \cite{Barrett}, such as jump discontinuities across the interface. Phase-field models replace sharp-interfaces by thin transitions regions where the interfacial forces are smoothly distributed (diffuse interfaces). For this reason, phase-field models are also referred to as \emph{diffuse interface} models, and they are emerging as a promising tool to treat problems with interfaces.  

From the mathematical point of view, the Cahn-Hilliard equation is a stiff, fourth-order, nonlinear parabolic partial differential equation. The elementary form of the Cahn-Hilliard equation is given by

\begin{equation}
    \frac{\partial \phi}{\partial t}=\nabla \cdot \left(m\left(\phi\right) \nabla \left(W'\left(\phi\right) -\epsilon  ^2 \Delta \phi \right)  \right)
    \label{element}
\end{equation} 


where $$\phi\left(\mathbf{x},t\right) \in [-1,1]$$ represents the phase-field variable, which describes the location of different components (e.g., $$\phi=-1$$ in oil and $$\phi=1$$ in water), $$m\left(\phi\right)$$ is the mobility, $$W\left(\phi\right)$$ is the so-called double-well potential, and $$\epsilon$$ is a length scale related to the thickness of the diffuse interface. 

Two different approaches have been used to solve the Cahn-Hilliard equation: solving the original form given by Eqn.\eqref{element}, which involves fourth-order operators, or by splitting it into two second order partial differential equations by introducing an auxiliary variable --- the chemical potential $$\mu$$. The split version of the equation is given by

\begin{equation}
    \frac{\partial \phi}{\partial t}=\nabla \cdot \left(m\left(\phi\right) \nabla \mu \right)
    \label{split1}
\end{equation}
\begin{equation}
\mu=W'\left(\phi \right) - \epsilon^2 \Delta \phi.
\label{chempot}
\end{equation}

The splitting strategy was proposed by Elliot \cite{Elliott1989ASO} to avoid constraints related to the continuity of the basis functions when using the finite element method with a primal formulation. It also facilitates the imposition of the boundary conditions on a circular geometry, which is the case we are interested in. Unfortunately, this comes at a price of an additional degree of freedom introduced into the solver. Nevertheless, this reformulation reduces the complexity of the problem from the numerical point of view (see \cite{M2AN_2009__43_5_1003_0,Zee}).

The spatial discretization of the governing equations is performed using isogeometric analysis (IGA) \cite{HUGHES20054135}. IGA is a generalization of the finite-element method that uses non-uniform rational B-splines (NURBS) to define the discrete spaces. A significant advantage of IGA with respect to finite element analysis is that the basis functions can be constructed with controllable continuity across the element boundaries, even on mapped geometries. The higher-order global continuity of the basis functions has been shown to produce higher accuracy than classical $$\mathcal{C}^0$$-continuous finite elements for the same number of degrees of freedom \cite{akkerman2008role,evans2009n}; and has been widely used to solve partial differential equations with high-order spatial derivatives \cite{GOMEZ20084333, GOMEZ20101828, GOMEZ201252}. Here, we will use $$\mathcal{C}^1$$-continuous quadratic splines for $$\phi$$ and $$\mu$$.
## Strong form
The strong form of the problem is formulated as follows: find $$\phi:\Omega \times \left[0,T\right]\rightarrow \mathbb{R}$$ and $$\mu:\Omega \times \left[0,T\right]\rightarrow \mathbb{R}$$ (being $$\mu$$ an  auxiliary variable) such that:

\begin{equation}
    \frac{\partial \phi}{\partial t}=\nabla \cdot \left(m\left(\phi\right) \nabla \mu\right) \quad \text{in} \ \Omega \times \left[0,T\right],  \label{st1}
\end{equation}   
\begin{equation}
    \mu=W'\left(\phi\right)-\epsilon^2 \Delta \phi \quad \text{in} \ \Omega \times \left[0,T\right], \label{st2}
\end{equation} 
\begin{equation} 
    \phi=g \quad \text{on} \ \Gamma_g \times \left[0,T\right], \label{st3} 
\end{equation} 
\begin{equation}    
    m\left(\phi\right)\epsilon^2\Delta\phi=q \quad \text{on} \ \Gamma_q \times \left[0,T\right], \label{st4}
\end{equation} 
\begin{equation}
    \nabla\left(m\left(\phi\right)\mu\right)\cdot \mathbf{n}=s \quad \text{on} \ \Gamma_s \times \left[0,T\right], \label{st5}
\end{equation} 
\begin{equation}
    \nabla\left(m\left(\phi\right)\phi\right)\cdot \mathbf{n}=h \quad \text{on} \ \Gamma_h \times \left[0,T\right], \label{st6}  
\end{equation} 
\begin{equation}
    \phi\left(\mathbf{x},0\right)=\phi_0\left(\mathbf{x}\right) \quad \text{in} \ \Omega. \label{st7}  
\end{equation} 

The double well function $$W\left(\phi\right)$$ is defined such that it has two local minima, which makes possible the coexistence of the different phases. Some important examples of double well functions can be found in \cite{Gomez2}. In this work we will take the classical quartic potential

\begin{equation}
    W\left(\phi\right)=\frac{1}{4}\left(1-\phi^2\right)^2,
\end{equation} 

which is a qualitative approximation of the logarithmic double well.

The mobility $$m\left(\phi\right)$$, which can be linked with the diffusivity, controls the time scale of the problem. The most common approach is to set it as a constant, $$m\left(\phi\right)=m$$. Such an approach is extensively applied in both analytical and numerical studies \cite{Rajagopal,polymer,CuetoFelgueroso2008ATF}. We will take $$m$$ constant and equal to one as recommended in \cite{GOMEZ20084333}.

The parameter $$\epsilon$$ is a positive constant that defines the length scale for the problem. According to \cite{GOMEZ20084333}, the solution to the Cahn-Hilliard equations depends only on the dimensionless number

\begin{equation}
    \alpha=\frac{L_0^2}{3\epsilon^2}
\end{equation}

also referred to as sharpness parameter, where $$L_0$$ is a length scale of the problem. Here, we will assume that $$L_0$$ is a measure of the computational domain size. Without loss of generality, $$L_0=R_2=1.0$$ will be the outer radius of the quarter of annulus. The sharpness parameter $\alpha$ usually takes values in the range $$10^3-10^4$$ \cite{GOMEZ20084333,Gomez2}. We will study the evolution of the phase-field variable for different values of $$\alpha$$.

## Results
We consider the split form of the Cahn-Hilliard equation on an open quarter-annulus domain
\begin{equation}
    \Omega = \left\{ (x,y) \in \mathbb{R}^2 : x > 0, y > 0, R_1^2 < x^2 + y^2 < R_2^2 \right\},
\end{equation}
with inner radius $$R_1=0.5$$ and outer radius $$R_2=1$$. We employ a computational mesh comprised of $$128^2$$ $$\mathcal{C}^1$$-quadratic elements; see the figure below. 

<div class="container">
    <div class="row justify-content-center mt-3">
        <div class="col mt-3 mt-md-0 d-flex justify-content-center">
            <div style="width: 50%;"> <!-- Container div to control width -->
                {% include figure.liquid loading="eager" path="assets/img/mesh.jpg" class="img-fluid rounded z-depth-1" %}
            </div>
        </div>
    </div>
    <div class="caption text-center">
        Geometry definition and mesh used for the calculations. The circular inset shows a detail of the mesh.
    </div>
</div>

The usual setup for numerical simulations of the Cahn-Hilliard equation is as follows: a randomly
perturbed homogeneous solution is allowed to evolve in a sufficiently large computational domain with periodic boundary conditions. Periodic boundary conditions would make no sense in our case, since we are not considering a square domain. Instead, we prescribe free-flux boundary conditions on the entire domain for $$\phi$$ and $$\mu$$. The initial condition is given by
\begin{equation}
    \phi_0\left(\mathbf{x}\right)=\bar{\phi}+r
\end{equation}
where $$\bar{\phi}$$ is a constant (referred to as the volume fraction) and $$r$$ is a random variable with uniform distribution in $$[-0.05,0.05]$$.

With this numerical setup we present two test cases which are defined by the sharpness parameter $\alpha$ and the volume fraction $$\bar{\phi}$$. We take $$\alpha=1500$$, $$\bar{\phi}=0.3$$ for the first case, and $$\alpha=3000$$, $$\bar{\phi}=0.1$$ for the second case.

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/fig2_ch.jpg" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/fig3_ch.jpg" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Evolution of the phase-field from a randomly perturbed initial condition. Left and right show the snapshots over time for different initial conditions. 
</div>

## Conclusions 
We presented a numerical methodology to solve the Cahn-Hilliard equation on a quarter-annulus domain. Our computational method is based on isogeometric analysis, which allows us to generate the $$\mathcal{C}^1$$-continuous functions required to solve this equation in a variational framework. We adopt the split form of the equation to reduce its order, and facilitate the imposition of the boundary conditions on the circular geometry. Time discretazion is performed using the generalized $$\alpha$$-methods, which provides second order accuracy and $$A$$-stability. We analyzed the solution over time for different values of $$\alpha$$ and $$\bar{\phi}$$. The parameter $$\alpha$$ affects the thickness of the interface and the time scale of the problem. As we increased $$\alpha$$, the separation process was faster, and the thickness of the interface became thinner. The initial volume fraction $$\bar{\phi}$$ modifies the topology of the solution. Smaller values of $$\bar{\phi}$$ produce more continuous patterns without nucleation.
