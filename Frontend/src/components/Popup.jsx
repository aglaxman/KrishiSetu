import React, { useState, useEffect } from "react";
import styles from "../assets/styles/Popup.module.css";
import ad from '../assets/images/ad.jpeg'

export const Popup = () => {
  const [show, setShow] = useState(false);

  // Show popup automatically on page load
  useEffect(() => {
    setShow(true);
  }, []);

  if (!show) return null;

  return (
    <div className={styles.overlay}>
      <div className={styles.modalDialog}>
        {/* Header */}

        <div className={styles.modalHeader}>
          <button className={styles.closeBtn} onClick={() => setShow(false)}>
            &times;
          </button>
        </div>

        {/* Body */}
        <div className={styles.modalBody}>
          <div className={styles.ad}>
            <img
              src={ad}
              alt="Ad"
            />
          </div>
          <div className={styles.details}>
            <div className={styles.heading}>
              <div className="logo"></div>
              <div className="off"></div>
            </div>
            <h2 className={styles.krishiBoost}  >KrishiBoost</h2>
            <h4>Boost Your Crop Yield! 🌾</h4>
            <p className={styles.textMuted} style={{fontSize:'18px'}}>
              Premium Fertilizer for Healthy & Abundant Harvests
              <br />
              Get <strong style={{fontSize:'20px',fontWeight:'bolder', color:'red'}}>20%</strong> Off on Your First Purchase!
            </p>
            <p className={styles.textMuted} style={{fontSize:'18px'}}>

              <strong>Special Offer:</strong> <strong style={{fontSize:'20px',fontWeight:'bolder', color:'red'}}>₹499 per 25kg bag</strong> 
            </p>

            <div className={`${styles.textMuted} ${styles.hurry}`} style={{fontSize:'20px'}}>
              Hurry. Buy now. Limited time offer
            </div>

            <div className={styles.bookingButtons}>
              <button className={`${styles.booking} ${styles.blinkButton}`}>
                <label>
                  <strong>Buy Now</strong>  
                  {/* <br />
                  <small className={styles.textMuted} style={{color:"whitesmoke"}}>Online</small> */}
                </label>
              </button>

              
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
