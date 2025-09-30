import React from "react";
import { FaFacebookF, FaTwitter, FaGoogle, FaInstagram, FaWeight } from "react-icons/fa";

export const Footer = () => {
  return (
    <footer className="text-lg-start text-white" style={{ backgroundColor: "#45526e", fontSize: "15px", width: "100%" }}>
      {/* Full-width container */}
      <div className="container-fluid ps-5">
        {/* Grid row */}
        <div className="row">
          {/* Company */}
          <div className="col-md-3 col-lg-3 col-xl-3 mx-auto mt-3">
            <h6 className="text-uppercase mb-4 font-weight-bold" style={{fontWeight:'900' , fontSize:'20px'}}>🌿 Kirishisetu</h6>
            <p>
              Kirishisetu is a digital platform empowering farmers to sell their produce directly to consumers, ensuring fair prices, transparency, and sustainability.
            </p>
          </div>

          <hr className="w-100 clearfix d-md-none" />

          {/* Products / Services */}
          <div className="col-md-2 col-lg-2 col-xl-2 mx-auto mt-3">
            <h6 className="text-uppercase mb-4 font-weight-bold">Products</h6>
            <p><a className="text-white" href="#">Farm Produce</a></p>
            <p><a className="text-white" href="#">Dairy & Meat</a></p>
            <p><a className="text-white" href="#">Organic Goods</a></p>
            <p><a className="text-white" href="#">Seeds & Fertilizers</a></p>
          </div>

          <hr className="w-100 clearfix d-md-none" />

          {/* Useful Links */}
          <div className="col-md-3 col-lg-2 col-xl-2 mx-auto mt-3">
            <h6 className="text-uppercase mb-4 font-weight-bold">Useful Links</h6>
            <p><a className="text-white" href="#">About Us</a></p>
            <p><a className="text-white" href="#">Contact</a></p>
            <p><a className="text-white" href="#">Privacy Policy</a></p>
            <p><a className="text-white" href="#">Terms & Conditions</a></p>
          </div>

          <hr className="w-100 clearfix d-md-none" />

          {/* Contact */}
          <div className="col-md-4 col-lg-3 col-xl-3 mx-auto mt-3">
            <h6 className="text-uppercase mb-4 font-weight-bold">Contact</h6>
            <p> Bengaluru, Karnataka, India</p>
            <p>support@krishisetu.com</p>
            <p> +91 98765 43210</p>
          </div>
        </div>
        {/* End Grid row */}

        <hr className="my-3" />

        {/* Bottom row */}
        <div className="row d-flex align-items-center">
          <div className="col-md-7 col-lg-8 text-center text-md-start">
            <div className="p-3">
              © 2025 Kirishisetu. All Rights Reserved.
            </div>
          </div>

          {/* Social Icons */}
          <div className="col-md-5 col-lg-4 text-center text-md-end">
            <a className="btn btn-outline-light btn-floating m-1" href="#" role="button">
              <FaFacebookF size={20} />
            </a>
            <a className="btn btn-outline-light btn-floating m-1" href="#" role="button">
              <FaTwitter size={20} />
            </a>
            <a className="btn btn-outline-light btn-floating m-1" href="#" role="button">
              <FaGoogle size={20} />
            </a>
            <a className="btn btn-outline-light btn-floating m-1" href="#" role="button">
              <FaInstagram size={20} />
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};
