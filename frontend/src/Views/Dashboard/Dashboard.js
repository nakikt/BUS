import './Dashboard.scss'
import Header from '../../Components/Header/Header';
import HousesTable from '../../Components/HousesTable/HousesTable';

const Dashboard = props => {
    return (
        <div className="Dashboard">
            <Header 
                user={props.user} setUser={props.setUser}
                isLoggedIn={props.isLoggedIn} setIsLoggedIn={props.setIsLoggedIn}
                setIsLogging={props.setIsLogging}
            />
            <HousesTable isLoggedIn={props.isLoggedIn}/>
        </div>
    );
}
 
export default Dashboard;