import { Link } from "react-router-dom";
// import { plusSymbol} from 
// import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";



const Home= () =>{

    const [data, setData] = useState([])  
    const [filteredData, setFilteredData] = useState([])  
    useEffect(() => {
        fetch("http://64.227.168.53:5000/api/read", {mode:'cors'})
            .then(response => {
                return response.json()
            })
        
            .then(data => {
                setData(data);
                setFilteredData(data);
            })
    }, [])
    console.log(data["data"]);

    const backgroundColorList = [
        "#8ac92638",
        "#ffb8032e",
        "#d6282839"
    ];
    const borderColorList = [
        "#8ac926",
        "#ffb703",
        "#d62828"
    ];

    const additionTask = (event) => {
        const titleGet = event.target.parentElement.parentElement.children[0].children[0].value;
        const descGet = event.target.parentElement.parentElement.children[1].children[0].value;
        const typeGet = event.target.parentElement.children[0].value;
        const deadlineGet = event.target.parentElement.children[1].value;
        let object = {
            "date": "2023-04-01",
            "deadline": deadlineGet,
            "title": titleGet,
            "type": typeGet,
            "description": descGet,
            "progress": 1
            };            
            data["data"].push(object);
            console.log(data["data"]);
    }
    fetch("http://64.227.168.53:5000/api/read", {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
           "Content-type": "application/json; charset=UTF-8"
        }
     })

    return (
        <div className="mainHome">
            <div className="selectMain">
                <div>
                    <a href=""><i class="fa-regular fa-square-plus"></i></a>
                    <h2>New Task</h2>
                </div>
                <select name="courses" id="courses" className="selectCourse">
                    <option value="all">All Tasks</option>
                    <option value="upcoming">Upcoming</option> 
                    <option value="present">Present</option> 
                    <option value="Done">Finsihed</option> 
                    <option value="overdue">Overdue</option>
                </select>
            </div>
            <div className="taskHolder">
                        <div className="task inputTask">
                            <div className="titleTask">
                                <input type="text" placeholder="title"/>
                                <h3>2023-04-01</h3>
                            </div>
                            <div className="contentDiv">
                                <textarea name="" id="" cols="30" rows="8" placeholder="description"></textarea>
                            </div>
                            <div className="deadlineTask">
                                <input type="text" placeholder="type"/>
                                <input type="text" placeholder="deadline"/>
                                <button onClick={additionTask}>Add</button>
                            </div>
                        </div>
            {
                data["data"]&&
                data["data"].map(pRec => {
                     
                    return (
                        <div className="task" style={{
                            backgroundColor: backgroundColorList[pRec.progress],
                            borderColor: borderColorList[pRec.progress]
                           }}>
                            <div className="titleTask">
                                <h1>{pRec.title}</h1>
                                <h3>{pRec.date}</h3>
                            </div>
                            <div className="contentDiv">
                                <p>{pRec.description}</p>
                            </div>
                            <div className="deadlineTask">
                                <h3>{pRec.type}</h3>
                                <h3>{pRec.deadline}</h3>
                            </div>
                        </div>
                    )
                })    
            }
                
            </div>
        </div>
    );
  }
  export default Home;