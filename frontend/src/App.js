import React, { Component } from 'react';
import axios from 'axios';


export default class App extends Component {
    render() {
        return (
            <div>
                <Todo />
            </div>
        )
    }
}

class Todo extends Component {
    constructor(){
        super();
        this.state = {
            todos: []
        };
    }
    componentDidMount () {
        axios.get("http://localhost:8000/api/v1/todo/")
        .then(resp => { this.setState({todos: resp.data}) });
    }
    render() {
        let todos = this.state.todos;
        if (todos.length > 0){
        return (
            <ul>
                { todos.map( todo => {return <li key={todo.id}> {todo.header} </li>} )}
            </ul>
        )
        } else {
            return <div>Loading...</div>
        }
    }
}