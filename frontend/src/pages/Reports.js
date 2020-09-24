import React from 'react';

// export const Reports  = () =>(
const Reports = () =>(
    <div>
        <h2>Senior Design Project Reports</h2>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gridGap: 20 }}>
            <div style={{display: 'flex',  justifyContent:'center', alignItems:'center'}}>
                <p>Our Project Proposal:  
                <a  href="https://docs.google.com/document/d/1ZlsD-6TjKa_ztcnagrnewWZ4UMxnRwC1xuEvjuwLwCE/edit?usp=sharing"> Click Here</a>
                </p>
            </div>
            <div><img src={require('../assets/Project_Proposal_img.png')} alt="" height="700"></img></div>
        </div>

        <p></p>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gridGap: 20 }}>
            <div style={{display: 'flex',  justifyContent:'center', alignItems:'center'}}>
                <p>Our Project Definition:  
                <a href="https://docs.google.com/document/d/1yLOBlV--6VprLL5PXlqcZhWf08FWEHsnPWvyHlyCTMY/edit?usp=sharing"> Click Here</a>
                </p>
            </div>
            <div><img src={require('../assets/Project_Definition_img.png')} alt="" height="700"></img></div>
        </div>

        <p></p>

        
        <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gridGap: 20 }}>
            <div style={{display: 'flex',  justifyContent:'center', alignItems:'center'}}>
                <p>Our System Design Report:  
                <a href="https://docs.google.com/document/d/1NnsUV5Lw5Y5NW-nRKLcS6hrLVwCTsCZ_O_ghkilDHQ4/edit?usp=sharing"> Click Here</a>
                </p>
            </div>
            <div><img src={require('../assets/System_Design_Report_img.png')} alt="" height="700"></img></div>
        </div>
        

        <p></p>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gridGap: 20 }}>
            <div style={{display: 'flex',  justifyContent:'center', alignItems:'center'}}>
                <p>Our Updated System Design Report:  
                <a href="https://docs.google.com/document/d/1Ar8vz3wwhaP3VM74Zco3-u2WcxzkhTwbDS4CzAjmT4I/edit?usp=sharing"> Click Here</a>
                </p>
            </div>
            <div><img src={require('../assets/Updated_System_Design_img.png')} alt="" height="700"></img></div>
        </div>
    </div>
)

export default Reports;
