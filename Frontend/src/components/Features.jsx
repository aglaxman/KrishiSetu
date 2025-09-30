import React from 'react';
import { FiUsers, FiShoppingCart } from "react-icons/fi";
import { MdLocalGroceryStore, MdSecurity } from "react-icons/md";
import { AiOutlineDollar } from "react-icons/ai";
import { IoMdNotificationsOutline } from "react-icons/io";
import { GiPriceTag } from "react-icons/gi";

export const Features = () => {
  const features = [
    { icon: <FiUsers size={50} className="text-primary mb-3" />, title: "Farmer-Buyer Connect", desc: "Connect farmers directly with buyers for better transparency and fair trade." },
    { icon: <MdLocalGroceryStore size={50} className="text-success mb-3" />, title: "Product Catalog", desc: "Browse a wide range of agricultural products with details and pricing." },
    { icon: <AiOutlineDollar size={50} className="text-warning mb-3" />, title: "Fair Pricing", desc: "Ensuring fair prices for both farmers and buyers through real-time market rates." },
    { icon: <FiShoppingCart size={50} className="text-info mb-3" />, title: "Online Orders", desc: "Order products online with easy checkout and secure payment options." },
    { icon: <GiPriceTag size={50} className="text-danger mb-3" />, title: "Deals & Offers", desc: "Get exclusive deals and discounts on selected products." },
    { icon: <MdSecurity size={50} className="text-secondary mb-3" />, title: "Secure Payments", desc: "All transactions are encrypted and fully secure for peace of mind." },
    { icon: <IoMdNotificationsOutline size={50} className="text-primary mb-3" />, title: "Real-Time Updates", desc: "Stay updated with notifications for orders, deals, and market alerts." },
  ];

  return (
    <section id="features" className="py-5 bg-light slide-up">
      <div className="container">
        <h2 className="fw-bold text-center mb-5">Key Features</h2>
        <div className="row text-center g-4">
          {features.map((feature, index) => (
            <div className="col-md-4 d-flex justify-content-center" key={index}>
              <div className="card p-4 shadow-sm h-100 d-flex flex-column align-items-center text-center">
                {feature.icon}
                <h5>{feature.title}</h5>
                <p>{feature.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};
