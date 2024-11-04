import React, { useState } from "react";
import SelectionPage from "./Components/SelectionPage";
import ResultPage from "./Components/ResultPage";


const App = () => {
	const [step, setStep] = useState(1);
	const [selectedAlgorithm, setSelectedAlgorithm] = useState(null);
	const [maxIteration, setMaxIteration] = useState(100);
	const [population, setPopulation] = useState(100);

	const handleSelectAlgorithm = (algorithm, max_iteration, populations) => {
		setSelectedAlgorithm(algorithm);
		setMaxIteration(max_iteration);
		setPopulation(populations);
		setStep(2);
	};

	return (
		<div className="min-h-screen bg-gradient-to-br from-indigo-100 via-purple-100 to-pink-100">
			{step === 1 ? (
				<SelectionPage onSelectAlgorithm={handleSelectAlgorithm} />
			) :(
				<ResultPage
					selectedAlgorithm={selectedAlgorithm}
					maxIteration={maxIteration}
					population={population}
				/>
			)}
		</div>
	);
};

export default App;
