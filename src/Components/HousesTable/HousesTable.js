import './HousesTable.scss'
import { MdEdit } from 'react-icons/md';
import { MdAddCircleOutline } from 'react-icons/md';
import database from './database';
import { useState } from 'react';

const HousesTable = props => {

    const [data, setData] = useState(database);
    const [isAdding, setIsAdding] = useState(false);
    const [addingValues, setAddingValues] = useState({'id': '','address': '','date': '','firstname': '','surname': '','state': ''});
    const [isAddingValuesCorrect, setIsAddingValuesCorrect] = useState(true);
    const [isEditing, setIsEditing] = useState(false);
    const [editingDataset, setEditingDataset] = useState();
    const [isIdUsedHook, setIsIdUsedHook] = useState();

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

        let isIdUsed = false;
        for (let i=0; i<data.length; i++) {
            if (addingValues.id == data[i].id) {
                isIdUsed = true;
            }
        }

        if(areAllFilledIn && !isIdUsed) {
            setIsAddingValuesCorrect(true);
            setIsIdUsedHook(false);
            setData([...data, {
                'id': addingValues.id, 
                'address': addingValues.address, 
                'date': addingValues.date, 
                'firstname': addingValues.firstname, 
                'surname': addingValues.surname, 
                'state': addingValues.state
            }]);
            setAddingValues({'id': '','address': '','date': '','firstname': '','surname': '','state': ''});
            setIsAdding(false);
        } else {
            if (!areAllFilledIn) {
                setIsAddingValuesCorrect(false);
            } else if (isIdUsed) {
                setIsIdUsedHook(true);
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
            let newData = [...data];
            newData[editingDataset.id] = {
                'id': addingValues.id, 
                'address': addingValues.address, 
                'date': addingValues.date, 
                'firstname': addingValues.firstname, 
                'surname': addingValues.surname, 
                'state': addingValues.state
            };
            setData(newData);
            setAddingValues({'id': '','address': '','date': '','firstname': '','surname': '','state': ''});
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
                            <th>Surname</th>
                            <th>State</th>
                            <th>Edit</th>
                        </tr>

                        {data.map((house) => 
                            <tr key={house.id}>
                                <td>{house.id}</td>
                                <td>{house.address}</td>
                                <td>{house.date}</td>
                                <td>{house.firstname}</td>
                                <td>{house.surname}</td>
                                <td>{house.state}</td>
                                <td>
                                    <button className={props.isLoggedIn ? 'edit' : 'edit not-logged-in'} onClick={() => handleEdit(house.id)}>
                                        <MdEdit />
                                    </button>
                                </td>
                            </tr>
                        )}
                        
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
                        {isIdUsedHook && <p>ID is already being used</p>}
                        <input type="text" value={addingValues.id} onChange={e => setAddingValues({...addingValues, id: e.target.value})}/>
                        <label>Address</label>
                        <input type="text" value={addingValues.address} onChange={e => setAddingValues({...addingValues, address: e.target.value})}/>
                        <label>Date</label>
                        <input type="text" value={addingValues.date} onChange={e => setAddingValues({...addingValues, date: e.target.value})}/>
                        <label>Name</label>
                        <input type="text" value={addingValues.firstname} onChange={e => setAddingValues({...addingValues, firstname: e.target.value})}/>
                        <label>Surname</label>
                        <input type="text" value={addingValues.surname} onChange={e => setAddingValues({...addingValues, surname: e.target.value})}/>
                        <label>State</label>
                        <input type="text" value={addingValues.state} onChange={e => setAddingValues({...addingValues, state: e.target.value})}/>
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
                            <label>Date</label>
                            <input type="text" value={addingValues.date} onChange={e => setAddingValues({...addingValues, date: e.target.value})}/>
                            <label>Name</label>
                            <input type="text" value={addingValues.firstname} onChange={e => setAddingValues({...addingValues, firstname: e.target.value})}/>
                            <label>Surname</label>
                            <input type="text" value={addingValues.surname} onChange={e => setAddingValues({...addingValues, surname: e.target.value})}/>
                            <label>State</label>
                            <input type="text" value={addingValues.state} onChange={e => setAddingValues({...addingValues, state: e.target.value})}/>
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