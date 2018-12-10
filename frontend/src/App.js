import React, { Component } from 'react';
import logo from './logo.svg';
import style from './App.module.scss';

class App extends Component {
	render() {
		return (
			<div className={style.App}>
				<header className={style.Appheader}>
					<img src={logo} className={style.Applogo} alt="logo" />
					<p>
						Edit <code>src/App.js</code> and save to reload.
					</p>
					<a
						className="App-link"
						href="https://reactjs.org"
						target="_blank"
						rel="noopener noreferrer"
					>
						Learn React
					</a>
				</header>
			</div>
		);
	}
}

export default App;
