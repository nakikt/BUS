import { useState } from 'react';
import './Dashboard.scss'
import Login from '../Login/Login'

const Dashboard = props => {

    const handleClick = () => {
        if(props.isLoggedIn) {
            props.setIsLoggedIn(false);
        } else {
            props.setIsLogging(true);
        }
        
    }

    return (
        <div className="Dashboard">
            <button className="login" onClick={handleClick}>
                {props.isLoggedIn ? "Log out" : "Login"}
            </button>
        </div>
    );
}
 
export default Dashboard;