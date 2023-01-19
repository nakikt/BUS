import './Header.scss'
import logo from '../../assets/logo2.png'

const Header = props => {
    
    const handleClick = () => {
        if(props.isLoggedIn) {
            props.setIsLoggedIn(false);
            props.setUser('');
        } else {
            props.setIsLogging(true);
        }
        
    }

    return (
        <div className="Header">
            <div className="container">
                <div className="inner">
                    <div className='wrapper'>
                        <img src={logo} alt='logo' className='logo'/>
                        <button onClick={() => props.setActiveSection('houses')}>Dashboard</button>
                        <button onClick={() => props.setActiveSection('history')}>History</button>
                    </div>
                    <div className='wrapper'>
                    {props.user!=='' && <h2 className="greeting">Welcome, {props.user}!</h2>}
                        <div className="btn">
                            <button className="login-btn" onClick={handleClick}>
                                {props.isLoggedIn ? "Log out" : "Login"}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
 
export default Header;