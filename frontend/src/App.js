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
			<header className="bg-gradient-to-r from-indigo-300 via-purple-400 to-indigo-200 text-white py-6 text-3xl font-bold text-center shadow-lg rounded-3xl animate-gradient">
				<div className="h-24 flex items-center justify-center relative">
					<h2 className="text-4xl font-bold bg-gradient-to-r from-purple-100 via-indigo-200 to-purple-100 bg-clip-text text-transparent">
						Magic Cube
					</h2>
				</div>
			</header>

			{step === 1 ? (
				<SelectionPage onSelectAlgorithm={handleSelectAlgorithm} />
			) : (
				<ResultPage
					selectedAlgorithm={selectedAlgorithm}
					maxIteration={maxIteration}
					population={population}
				/>
			)}
			<footer className="bg-white-200 text-center text-gray-700 py-4">
				&copy; 2024 EkaaPrawiraa, cupski, frdmm, rifchzschki. All rights
				reserved.
			</footer>
		</div>
	);
};

export default App;
