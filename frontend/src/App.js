import React, { useState } from "react"
import "./App.css"
import { Collapse } from "react-collapse"

/*
This app will give an easy to use 
*/

function App() {
	let [showForm, setShowForm] = useState(false)

	const handleSubmit = e => {
		e.preventDefault()
		console.log("Submit pressed")
	}

	return (
		<div>
			<h1>Meals on Wheels Spreadsheet Creator</h1>
			<div
				onClick={e => {
					e.preventDefault()
					setShowForm(!showForm)
				}}
			>
				Click here to add new person
			</div>

			<Collapse isOpened={showForm}>
				<form id="NameForm" onSubmit={handleSubmit}>
					Enter Name:
					<input type="text" />
					<button type="submit" form="NameForm">
						+
					</button>
				</form>
				<form id="StreetAddressForm" onSubmit={handleSubmit}>
					Enter Street Address:
					<input type="text" />
					<button type="submit" form="StreetAddressForm">
						+
					</button>
				</form>
        <form id="CityTownForm" onSubmit={handleSubmit}>
					Enter City or Town:
					<input type="text" />
					<button type="submit" form="CityTownForm">
						+
					</button>
				</form>
        <form id="StateForm" onSubmit={handleSubmit}>
					Enter State:
					<input type="text" />
					<button type="submit" form="StateForm">
						+
					</button>
				</form>
        <form id="MealForm" onSubmit={handleSubmit}>
					Enter Meal:
					<input type="text" />
					<button type="submit" form="MealForm">
						+
					</button>
				</form>
			</Collapse>
		</div>
	)
}

export default App
