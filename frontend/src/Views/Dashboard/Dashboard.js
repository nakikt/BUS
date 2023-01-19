import './Dashboard.scss'
import Header from '../../Components/Header/Header';
import HousesTable from '../../Components/HousesTable/HousesTable';
import History from '../../Components/History/History';
import { useState } from 'react';

const Dashboard = props => {

    const [activeSection, setActiveSection] = useState('houses');

    return (
        <div className="Dashboard">
            <Header 
                user={props.user} setUser={props.setUser}
                isLoggedIn={props.isLoggedIn} setIsLoggedIn={props.setIsLoggedIn}
                setIsLogging={props.setIsLogging}
                setActiveSection={setActiveSection}
            />
            {activeSection === 'houses' ? (
                <HousesTable isLoggedIn={props.isLoggedIn}/>
            ) : (
                <History />
            )}
        </div>
    );
}
 
export default Dashboard;