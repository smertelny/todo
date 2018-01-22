import React, {Component} from 'react';
import axios from 'axios';

const API_HOST = 'http://localhost:8000/'


export default class Todos extends Component {
    constructor(){
        super();
        this.state = {
            todos: []
        };
    }

    componentDidMount () {
        axios.get(API_HOST + "api/v1/todo/")
        .then(resp => { this.setState({todos: resp.data}) });
    }

    handleClick(data, index) {
        data = {...data, "isDone": !data.isDone}
        let result = window.confirm('Are you sure you wanna make it done?');
        if (result) {
            axios.put(API_HOST + 'api/v1/todo/' + data.id + "/",
                    data).then(console.log(...data))
                    .then(
                        () => {this.setState({
                        todos: [...this.state.todos.slice(0, index),
                               data,
                               ...this.state.todos.slice(index + 1)
                               ]})
                            }
                        );
        };
    }

    render() {
        let todos = this.state.todos;
        console.log(todos);
        return (
            <div>
                <ul>
                    { todos.map( (todo, index) => {return <Todo handleClick={this.handleClick.bind(this, todo, index)} key={index} data={todo} />} )}
                </ul>
                <AddTodo />
            </div>
        )
    }
}


class Todo extends Component {
    render() {
        const { data } = this.props;
        return <li><span style={data.isDone ? {textDecoration: 'line-through'}: {textDecoration:'none'}} onClick={this.props.handleClick} >{ data.header }</span> - {String(data.isDone)}</li>
    }
}

class AddTodo extends Component {
    constructor() {
        super();
        this.handleClick = this.handleClick.bind(this);
    }

    handleClick(e) {
        console.log(this.title);
        console.log(this.desc);
    }

    render() {
        return (<div>
                    <label htmlFor="title">Title:</label>
                    <input type="text" name="title"
                    ref={input => {this.title = input}} />
                    <br />
                    <label htmlFor="desc">Desc:</label>
                    <input type="text" name="desc"
                    ref={input => {this.desc = input}} />
                    <br />
                    <button onClick={this.handleClick}>Add Todo</button>
                </div>
        )
    }
}