import { useEffect, useState } from 'react';
import './History.scss'
import {TailSpin} from 'react-loader-spinner';

const History = () => {

    const [history, setHistory] = useState();
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        setIsLoading(true);
        fetch('http://localhost:5000/history').then(
            res => res.json()
          ).then(
            receivedData => {
                const sortedData = receivedData.sort((a, b) => a.time > b.time ? -1 : 1)
                setHistory(sortedData);
                setIsLoading(false);
            }
          )
    }, [])

    return (
        <div className="History">
            <div className="container">
                <table>
                    <tbody>
                        <tr>
                            <th>ID</th>
                            <th>Address</th>
                            <th>Date</th>
                            <th>Name</th>
                            <th>Condition</th>
                        </tr>

                        {history?.map((house, key) => 
                            <tr key={key}>
                                <td>{house.id}</td>
                                <td>{house.address}</td>
                                <td>{house.time}</td>
                                <td>{house.name_surname}</td>
                                <td>{house.condition}</td>
                            </tr>
                        )}

                        {isLoading && <tr><td>
                            <TailSpin
                                height="40"
                                width="40"
                                color="white"
                                ariaLabel="tail-spin-loading"
                                radius="1"
                                wrapperStyle={{
                                    'justifyContent': 'center'
                                }}
                                wrapperClass=""
                                visible={true}
                            />
                        </td></tr>}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
 
export default History;