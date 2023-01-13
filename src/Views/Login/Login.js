import './Login.scss'
import { useState } from 'react';
import logo from '../../assets/logo2.png'

const Login = props => {

    const [userLocal, setUserLocal] = useState('')
    const [pwd, setPwd] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (userLocal && pwd) {
            //TODO: check credentials here
            if(1) { //if credentials valid
                props.setIsLoggedIn(true);
                localStorage.setItem('user', userLocal);
                props.setUser(userLocal);
                setUserLocal('');
                setPwd('');
                props.setIsLogging(false);
            } else {
                console.log("Credentials invalid.")
            }
        } else {
            console.log('Please enter username and password.')
        }
    }

    return (
        <div className="Login">
            <img src={logo} alt='logo' className='logo'/>
            <div className="login-container">
                <h2 className="login-header">Login</h2>
                <form onSubmit={ handleSubmit }>
                    <label className="login-label">
                        User
                    </label>
                    <input value={ userLocal } type="text" className="user-input" onChange={(e) => setUserLocal(e.target.value)} />
                    <label className="pwd-label">
                        Password
                    </label>
                    <input value={ pwd } type="password" className="pwd-input" onChange={(e) => setPwd(e.target.value)} />
                    <input type="submit" className="submit" value="Submit" />
                </form>
            </div>
        </div>
    );
}
 
export default Login;