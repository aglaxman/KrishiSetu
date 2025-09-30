import React from 'react'

export const Features = () => {
  return (
    <>
        {/* <!-- Features Section --> */}
      <section id="features" className="py-5 bg-light slide-up">
        <div className="container">
          <h2 className="fw-bold text-center mb-5">Key Features</h2>
          <div className="row text-center g-4">
            <div className="col-md-4">
              <div className="card p-4 shadow-sm h-100">
                <i className="bi bi-megaphone fs-1 text-primary mb-3"></i>
                <h5>Complaint Management</h5>
                <p>Citizens register and track complaints, while admins resolve and update status in real-time.</p>
              </div>
            </div>
            <div className="col-md-4">
              <div className="card p-4 shadow-sm h-100">
                <i className="bi bi-cash-stack fs-1 text-success mb-3"></i>
                <h5>Transparent Donations</h5>
                <p>Donors contribute directly to causes and track how funds are utilized by the administration.</p>
              </div>
            </div>
            <div className="col-md-4">
              <div className="card p-4 shadow-sm h-100">
                <i className="bi bi-graph-up fs-1 text-warning mb-3"></i>
                <h5>Reports & Analytics</h5>
                <p>Admins generate reports, ensuring transparency and accountability for every action taken.</p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </>
  )
}
