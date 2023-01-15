import './HousesTable.scss'
import { MdEdit } from 'react-icons/md';
import { MdAddCircleOutline } from 'react-icons/md';
import { useEffect, useState } from 'react';
import {TailSpin} from 'react-loader-spinner';

const HousesTable = props => {

    const [data, setData] = useState();
    const [isAdding, setIsAdding] = useState(false);
    const [addingValues, setAddingValues] = useState({'id': '','address': '','name_surname': '','condition': ''});
    const [isAddingValuesCorrect, setIsAddingValuesCorrect] = useState(true);
    const [isEditing, setIsEditing] = useState(false);
    const [editingDataset, setEditingDataset] = useState();
    const [isIdNumeric, setIsIdNumeric] = useState(true);
    const [isIdUsedHook, setIsIdUsedHook] = useState();
    const [isLoading, setIsLoading] = useState(false);
    const [isFetchOk, setIsFetchOk] = useState(true);
    const [pullData, setPullData] = useState(0);

    useEffect(() => {
        fetch('http://localhost:5000/').then(
            res => res.json()
          ).then(
            receivedData => setData(receivedData)
          )
    },[pullData])

    const handleAdd = () => {
        setIsAdding(true);
    }

    const handleAddSubmit = e => {
        e.preventDefault();

        let areAllFilledIn = true;
        for (const value of Object.values(addingValues)) {
            if (value === '') {
                areAllFilledIn = false;
            }
        }

        let isIdNumericVariable = !isNaN(addingValues.id);

        let isIdUsed = false;
        for (let i=0; i<data.length; i++) {
            if (addingValues.id == data[i].id) {
                isIdUsed = true;
            }
        }

        if(areAllFilledIn && !isIdUsed && isIdNumericVariable) {
            setIsAddingValuesCorrect(true);
            setIsIdUsedHook(false);
            setIsIdNumeric(true);

            setIsLoading(true);

            // POST REQUEST HERE
            fetch('http://localhost:5000/add', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    'id': addingValues.id, 
                    'address': addingValues.address, 
                    'name_surname': addingValues.name_surname, 
                    'condition': addingValues.condition
                })
            }).then(
                response => {
                    response.json();
                    setIsFetchOk(true);
                    setIsLoading(false);
                    setPullData(current => current+1);                 
                }
            ).catch(error => {
                console.log(error);
                setIsFetchOk(false);
                setIsLoading(false);
            })

            // PULL DATA/REPOSNSE? AND DISPLAY
            // setData([...data, {
            //     'id': addingValues.id, 
            //     'address': addingValues.address, 
            //     'name_surname': addingValues.name_surname, 
            //     'condition': addingValues.condition
            // }]);


            setAddingValues({'id': '','address': '','name_surname': '','condition': ''});
            setIsAdding(false);
        } else {
            if (!areAllFilledIn) {
                setIsAddingValuesCorrect(false);
                setIsIdUsedHook(false);
                setIsIdNumeric(true);
            } else if (!isIdNumericVariable) {
                setIsIdNumeric(false);
                setIsAddingValuesCorrect(true);
            setIsIdUsedHook(false);
            } else if (isIdUsed) {
                setIsIdUsedHook(true);
                setIsAddingValuesCorrect(true);
                setIsIdNumeric(true);
            }
        }
    }

    const handleEditSubmit = e => {
        e.preventDefault();

        let areAllFilledIn = true;
        for (const value of Object.values(addingValues)) {
            if (value === '') {
                areAllFilledIn = false;
            }
        }

        if(areAllFilledIn) {
            setIsAddingValuesCorrect(true);

            fetch('http://localhost:5000/edit', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    'id': addingValues.id, 
                    'address': addingValues.address, 
                    'name_surname': addingValues.name_surname, 
                    'condition': addingValues.condition
                })
            }).then(
                response => {
                    response.json();
                    setIsFetchOk(true);
                    setIsLoading(false);
                    setPullData(current => current+1);                 
                }
            ).catch(error => {
                console.log(error);
                setIsFetchOk(false);
                setIsLoading(false);
            })

            setAddingValues({'id': '','address': '','name_surname': '','condition': ''});
            setIsEditing(false);
        } else {
                setIsAddingValuesCorrect(false);
        }
    }

    const handleEdit = passedId => {
        setIsEditing(true);

        let i;
        for (i=0; i<data.length; i++) {
            if (data[i].id === passedId) {
                break;
            }
        }

        setEditingDataset(data[i]);
        setAddingValues(data[i]);
    }

    return (
        <div className="HousesTable">
            <div className="container">
                <table>
                    <tbody>
                        <tr>
                            <th>ID</th>
                            <th>Address</th>
                            <th>Date</th>
                            <th>Name</th>
                            <th>Condition</th>
                            <th>Edit</th>
                        </tr>

                        {data?.map((house) => 
                            <tr key={house.id}>
                                <td>{house.id}</td>
                                <td>{house.address}</td>
                                <td>{house.date}</td>
                                <td>{house.name_surname}</td>
                                <td>{house.condition}</td>
                                <td>
                                    <button className={props.isLoggedIn ? 'edit' : 'edit not-logged-in'} onClick={() => handleEdit(house.id)}>
                                        <MdEdit />
                                    </button>
                                </td>
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

                        {!isFetchOk && <tr><td>Something went wrong, try again</td></tr>}
                        
                        {/* ADD HOUSE ROW BUTTON */}
                        <tr>
                            <td>
                                <button onClick={handleAdd} className={props.isLoggedIn ? 'add' : 'add not-logged-in'}>
                                    <MdAddCircleOutline />
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            {/* ADDING FORM */}
            <div className={isAdding ? "add-form-container visible" : "add-form-container"}>
                <div className="inner">
                    <form>
                        <label>ID</label>
                        {!isIdNumeric && <p className='alert visible'>ID has to be a number</p>}
                        {isIdUsedHook && <p className='alert visible'>ID is already being used</p>}
                        <input type="text" value={addingValues.id} onChange={e => setAddingValues({...addingValues, id: e.target.value})}/>
                        <label>Address</label>
                        <input type="text" value={addingValues.address} onChange={e => setAddingValues({...addingValues, address: e.target.value})}/>
                        <label>Name</label>
                        <input type="text" value={addingValues.name_surname} onChange={e => setAddingValues({...addingValues, name_surname: e.target.value})}/>
                        <label>Condition</label>
                        <input type="text" value={addingValues.condition} onChange={e => setAddingValues({...addingValues, condition: e.target.value})}/>
                        <p className={isAddingValuesCorrect ? 'alert' : 'alert visible'}>Fill in all the values</p>
                        <input type="submit" value={"Add"} className="submit-btn" onClick={handleAddSubmit}/>
                    </form>
                </div>
            </div>

            {/* EDITING FORM */}
            {isEditing &&
                <div className={isEditing ? "add-form-container visible" : "add-form-container"}>
                    <div className="inner">
                        <form>
                            <label>ID</label>
                            <input type="text" value={editingDataset.id} readOnly/>
                            <label>Address</label>
                            <input type="text" value={addingValues.address} onChange={e => setAddingValues({...addingValues, address: e.target.value})}/>
                            <label>Name</label>
                            <input type="text" value={addingValues.name_surname} onChange={e => setAddingValues({...addingValues, name_surname: e.target.value})}/>
                            <label>Condition</label>
                            <input type="text" value={addingValues.condition} onChange={e => setAddingValues({...addingValues, condition: e.target.value})}/>
                            <p className={isAddingValuesCorrect ? 'alert' : 'alert visible'}>Fill in all the values</p>
                            <input type="submit" value={"Save"} className="submit-btn" onClick={handleEditSubmit}/>
                        </form>
                    </div>
                </div>
            }
        </div>
    );
}
 
export default HousesTable;