import React, { useState } from "react"
import "./App.css"
import { Collapse } from "react-collapse"

/*
This app will give an easy to use 
*/

function App() {
  let [showForm, setShowForm] = useState(false)

	return (
		<div>
			<h1>Meals on Wheels Spreadsheet Creator</h1>
			<div onClick={(e) => {
        e.preventDefault()
        setShowForm(!showForm)
      }}>
        click here
      </div>
        
				<Collapse isOpened={showForm}>
					<form>
						Enter data:
						<input type="text" name="name" />
					</form>
				</Collapse>
			
		</div>
	)
}

export default App
