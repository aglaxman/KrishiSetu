import React, { useState, useEffect } from 'react';


import Typewriter from 'typewriter-effect';



export const HeroSection = () => {



  return (
    <section id="home" className="hero d-flex align-items-center text-center text-white">
      <div className="container fade-in">
        <h1 className="display-3 fw-bold">
        <Typewriter
        options={{ autoStart: true }}
        onInit={(typewriter) => {
          typewriter
            .typeString('<span style="color:#96A78D;">TRUST</span>')
            .pauseFor(1500)
            .deleteAll()
            .typeString('<span style="color:#96A78D;">FAIRNESS</span>')
            .pauseFor(1500)
            .deleteAll()
            .typeString('<span style="color:#96A78D;">TRANSPARENT</span>')
            .pauseFor(1500)
            .deleteAll()
            .typeString('<span style="color:#96A78D;">Welcome to </span><span style="color:#E62727;">KrishiSetu</span>')
            .pauseFor(2500)
            .start();
        }}
      />


        </h1>

        {/* <h1 className="display-3 fw-bold">{displayText}</h1> */}
        <p className="lead mt-3">
          Redefining agriculture by connecting farmers to consumers directly — transparent, fair, and sustainable.
        </p>
        <div className="mt-4 hero-btn">
          <a href="/sell" className="btn btn-outline-secondary btn-lg me-3 hero-sell">Sell Your Produce</a>
          <a href="/buy" className="btn btn-outline-secondary btn-lg hero-buy">Explore Produce</a>
        </div>
      </div>
    </section>
  );
};
