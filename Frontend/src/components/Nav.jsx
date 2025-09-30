import React from 'react'
import '../assets/styles/style.css'
const Nav = () => {
  return (
    <>
        {/* <!-- Navbar --> */}
        <nav class="navbar navbar-expand-lg navbar-dark custom-navbar fixed-top shadow">
            <div class="container">
            <a class="navbar-brand fw-bold" href="#">🌿 KrishiSetu</a>

            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto align-items-lg-center">
                <li class="nav-item"><a class="nav-link active" href="#home">Home</a></li>
                <li class="nav-item"><a class="nav-link" href="#about">About</a></li>
                <li class="nav-item"><a class="nav-link" href="#features">Features</a></li>
                <li class="nav-item"><a class="nav-link" href="#impact">Impact</a></li>

                {/* <!-- Login Dropdown --> */}
                <li class="nav-item dropdown ms-lg-3">
                    <a class="btn btn-outline-light " href="#" role="button" >
                    Login / Register
                    </a>
                    
                </li>

                        
                </ul>
            </div>
            </div>
        </nav>
    </>
  )
}

export default Nav