import React from 'react'
import Nav from '../components/Nav'
import { Footer } from '../components/Footer'
import homebg from '../assets/images/homebg.png'
import { HeroSection } from '../components/HeroSection'
import { About } from '../components/About'
import { Features } from '../components/Features'

export const Index = () => {
  return (
    <>
      
      <Nav/>
      <HeroSection/>
      <About/>
      <Features/>
      <Footer/>
    </>
  )
}
