import React, { useState } from "react";
const SelectionPage = ({ onSelectAlgorithm }) => {
	const [algorithm, setAlgorithm] = useState("");
	const [maxIteration, setMaxIteration] = useState(100);
	const [population, setPopulation] = useState(100);

	const algorithms = [
		{ value: "1", label: "Steepest Ascent Hill Climbing" },
		{ value: "2", label: "Random Restart Hill Climbing" },
		{ value: "3", label: "Sideways Hill Climbing" },
		{ value: "4", label: "Stochastic Hill Climbing" },
		{ value: "5", label: "Simulated Annealing" },
		{ value: "6", label: "Genetic Algorithm" },
	];

	return (
		<div className="min-h-screen bg-gradient-to-br from-indigo-100 via-purple-100 to-pink-100 p-8 flex items-center justify-center">
			<div className="max-w-lg w-full bg-white/90 backdrop-blur-md rounded-2xl shadow-2xl p-8 border border-white/20">
				<div className="space-y-6">
					<div className="text-center">
						<h2 className="text-4xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
							Algorithm
						</h2>
						<p className="mt-2 text-gray-600">
							Select your preferred algorithm and parameters
						</p>
					</div>

					<div className="space-y-4">
						<div className="relative">
							<select
								value={algorithm}
								onChange={(e) => setAlgorithm(e.target.value)}
								className="w-full px-4 py-3 rounded-lg bg-gray-50 border border-gray-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition-all appearance-none"
							>
								<option value="">Select algorithm</option>
								{algorithms.map((algo) => (
									<option key={algo.value} value={algo.value}>
										{algo.label}
									</option>
								))}
							</select>
							<div className="absolute right-3 top-1/2 transform -translate-y-1/2 pointer-events-none">
								<svg
									className="w-5 h-5 text-gray-400"
									fill="none"
									stroke="currentColor"
									viewBox="0 0 24 24"
								>
									<path
										strokeLinecap="round"
										strokeLinejoin="round"
										strokeWidth="2"
										d="M19 9l-7 7-7-7"
									/>
								</svg>
							</div>
						</div>

						{(algorithm === "2" || algorithm === "3" || algorithm === "6") && (
							<div className="space-y-4">
								{algorithm === "6" && (
									<div className="space-y-2">
										<label className="block text-sm font-medium text-gray-700">
											Population Size
										</label>
										<input
											type="number"
											value={population}
											onChange={(e) => setPopulation(Number(e.target.value))}
											className="w-full px-4 py-3 rounded-lg bg-gray-50 border border-gray-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition-all"
											placeholder="Enter population size"
										/>
									</div>
								)}
								<div className="space-y-2">
									<label className="block text-sm font-medium text-gray-700">
										{algorithm === "3"
											? "Maximum Sideways Move"
											: "Maximum Iterations"}
									</label>
									<input
										type="number"
										value={maxIteration}
										onChange={(e) => setMaxIteration(Number(e.target.value))}
										className="w-full px-4 py-3 rounded-lg bg-gray-50 border border-gray-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition-all"
										placeholder={
											algorithm === "3"
												? "Enter max sideways move"
												: "Enter max iterations"
										}
									/>
								</div>
							</div>
						)}

						<button
							className={`w-full py-3 px-4 rounded-lg font-medium transition-all duration-200 ${
								algorithm
									? "bg-gradient-to-r from-indigo-600 to-purple-600 text-white hover:from-indigo-700 hover:to-purple-700 transform hover:-translate-y-0.5"
									: "bg-gray-100 text-gray-400 cursor-not-allowed"
							}`}
							disabled={!algorithm}
							onClick={() =>
								onSelectAlgorithm(algorithm, maxIteration, population)
							}
						>
							Start Visualization
						</button>
					</div>
				</div>
			</div>
		</div>
	);
};

export default SelectionPage;