import React, { useState, useRef, useEffect } from "react";
import { Pause, Play, RotateCcw, LineChart as ChartIcon } from "lucide-react";
import {
	LineChart,
	Line,
	XAxis,
	YAxis,
	CartesianGrid,
	Tooltip,
	ResponsiveContainer,
} from "recharts";
import axios from "axios";

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
							Magic Cube Algorithm
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
										Maximum Iterations
									</label>
									<input
										type="number"
										value={maxIteration}
										onChange={(e) => setMaxIteration(Number(e.target.value))}
										className="w-full px-4 py-3 rounded-lg bg-gray-50 border border-gray-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition-all"
										placeholder="Enter max iterations"
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

const ResultPage = ({ selectedAlgorithm, maxIteration, population }) => {
	const [isPlaying, setIsPlaying] = useState(false);
	const [currentFrame, setCurrentFrame] = useState(0);
	const [playbackSpeed, setPlaybackSpeed] = useState(1);
	const [cubeStates, setCubeStates] = useState([]);
	const [totalFrames, setTotalFrames] = useState(0);
	const [totalTime, setTotalTime] = useState(0);
	const [isLoading, setIsLoading] = useState(false);
	const [previousFrame, setPreviousFrame] = useState(null);
	const [showPlot, setShowPlot] = useState(false);
	const [totalFreq, setTotalFreq] = useState([]);

	useEffect(() => {
		const fetchData = async () => {
			setIsLoading(true);
			try {
				const payload = {
					algorithm: Number(selectedAlgorithm),
					...(selectedAlgorithm === "2" || selectedAlgorithm === "3"
						? { max_iteration: maxIteration }
						: {}),
					...(selectedAlgorithm === "6"
						? { max_iteration: maxIteration, population }
						: {}),
				};

				const response = await axios.post(
					"http://localhost:8000/api/receive-cube/",
					payload
				);
				const data = response.data;
				setCubeStates(data.result);
				setTotalTime(data.total_time);
				setTotalFrames(data.result.length);
				setCurrentFrame(0);
				if (data.total_freq) {
                    setTotalFreq(data.total_freq);
                }
				setIsPlaying(false);
			} catch (error) {
				console.error("Error fetching data:", error);
			} finally {
				setIsLoading(false);
			}
		};
		fetchData();
	}, [selectedAlgorithm, maxIteration, population]);

	useEffect(() => {
		setPreviousFrame(currentFrame > 0 ? cubeStates[currentFrame - 1] : null);
	}, [currentFrame, cubeStates]);

	const getCellColor = (value, layerIndex, rowIndex, colIndex) => {
		const baseColors = {
			0: "from-rose-100 to-rose-200",
			1: "from-blue-100 to-blue-200",
			2: "from-teal-100 to-teal-200",
			3: "from-amber-100 to-amber-200",
			4: "from-purple-100 to-purple-200",
		};
		if (previousFrame && previousFrame[1]) {
			const prevValue = previousFrame[1][layerIndex][rowIndex][colIndex];
			if (prevValue !== value) {
				return "from-pink-500 to-rose-600 animate-pulse";
			}
		}

		return baseColors[layerIndex];
	};

	const getPlotData = () => {
		return cubeStates.map((state) => ({
			iteration: state[0],
			score: state[2],
		}));
	};

	const getSimulatedAnnealingData = () => {
        return cubeStates.map((state) => ({
            iteration: state[0],
            probability: state[4] || 0,     // probability (flag) is at index 4 if exists
        }));
    };

	const renderPlot = () => (
		<div className="fixed inset-0 bg-black/50 flex items-center justify-center p-8">
			<div className="bg-white rounded-2xl p-8 w-full max-w-4xl">
				<div className="flex justify-between items-center mb-4">
					<h3 className="text-xl font-bold text-gray-800">
						{selectedAlgorithm === "5" ? "Simulated Annealing Plot" : "Objective Function Plot"}
					</h3>
					<button
						onClick={() => setShowPlot(false)}
						className="p-2 hover:bg-gray-100 rounded-full"
					>
						×
					</button>
				</div>
				<div className={`${selectedAlgorithm === "5" ? 'grid grid-cols-2 gap-6' : ''} h-96`}>
				{/* Objective Function Plot */}
				<div className="h-full">
					<h4 className="text-lg font-semibold text-gray-700 mb-2 text-center">
					Objective Function
					</h4>
					<ResponsiveContainer width="100%" height="90%">
					<LineChart
						data={getPlotData()}
						margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
					>
						<CartesianGrid strokeDasharray="3 3" />
						<XAxis
						dataKey="iteration"
						label={{ value: "Iterations", position: "bottom", offset: 0 }}
						/>
						<YAxis
						label={{ value: "Score", angle: -90, position: "insideLeft" }}
						/>
						<Tooltip />
						<Line
						type="monotone"
						dataKey="score"
						stroke="#6366f1"
						strokeWidth={2}
						dot={false}
						name="Score"
						/>
					</LineChart>
					</ResponsiveContainer>
				</div>

				{/* Simulated Annealing Metrics */}
				{selectedAlgorithm === "5" && (
					<div className="h-full">
					<h4 className="text-lg font-semibold text-gray-700 mb-2 text-center">
						Probability plot
					</h4>
					<ResponsiveContainer width="100%" height="90%">
						<LineChart
						data={getSimulatedAnnealingData()}
						margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
						>
						<CartesianGrid strokeDasharray="3 3" />
						<XAxis
							dataKey="iteration"
							label={{ value: "Iterations", position: "bottom", offset: 0 }}
						/>
						{/* Left Y-Axis for Probability */}
						<YAxis
							label={{ value: "Probability", angle: -90, position: "insideLeft" }}
							domain={[0, 1]}  // Probability values are between 0 and 1
						/>
						<Tooltip />
						<Line
							type="monotone"
							dataKey="probability"
							stroke="#10b981"
							strokeWidth={2}
							dot={false}
							name="Probability"
						/>
						</LineChart>
					</ResponsiveContainer>
					</div>
				)}
				</div>

				<div className="mt-4 flex justify-center gap-6">
				<div className="flex items-center gap-2">
					<div className="w-4 h-4 bg-indigo-500 rounded-full"></div>
					<span className="text-sm text-gray-600">Score</span>
				</div>
				{selectedAlgorithm === "5" && (
					<div className="flex items-center gap-2">
					<div className="w-4 h-4 bg-emerald-500 rounded-full"></div>
					<span className="text-sm text-gray-600">Probability</span>
					</div>
				)}
				</div>
			</div>
		</div>
	);
	const togglePlayPause = () => setIsPlaying(!isPlaying);

	useEffect(() => {
		if (isPlaying) {
			const interval = setInterval(() => {
				setCurrentFrame((prev) => {
					if (prev >= totalFrames - 1) {
						setIsPlaying(false);
						return prev;
					}
					return prev + 1;
				});
			}, 1000 / playbackSpeed);

			return () => clearInterval(interval);
		}
	}, [isPlaying, totalFrames, playbackSpeed]);

	const renderCubeLayer = (layer, layerIndex) => (
		<div key={layerIndex} className="mb-8">
			<h4 className="text-sm font-medium text-gray-600 mb-3">
				Layer {layerIndex + 1}
			</h4>
			<div className="grid grid-cols-5 gap-3">
				{layer.map((row, rowIndex) =>
					row.map((cell, colIndex) => (
						<div
							key={`${layerIndex}-${rowIndex}-${colIndex}`}
							className={`w-14 h-14 flex items-center justify-center bg-gradient-to-br ${getCellColor(
								cell,
								layerIndex,
								rowIndex,
								colIndex
							)} rounded-xl shadow-lg text-white font-medium transform transition-all duration-200 hover:scale-110 hover:rotate-3`}
						>
							{cell}
						</div>
					))
				)}
			</div>
		</div>
	);

	if (isLoading) {
		return (
			<div className="min-h-screen bg-gradient-to-br from-indigo-100 via-purple-100 to-pink-100 flex items-center justify-center">
				<div className="relative w-24 h-24">
					<div className="absolute top-0 left-0 w-full h-full border-4 border-indigo-200 rounded-full animate-pulse"></div>
					<div className="absolute top-0 left-0 w-full h-full border-4 border-indigo-500 rounded-full animate-spin border-t-transparent"></div>
				</div>
			</div>
		);
	}

	return (
		<div className="min-h-screen bg-gradient-to-br from-indigo-100 via-purple-100 to-pink-100 p-8">
			<div className="max-w-4xl mx-auto bg-white/90 backdrop-blur-md rounded-2xl shadow-2xl p-8 border border-white/20">
				<div className="space-y-8">
					<div className="text-center">
						<h2 className="text-4xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
							Magic Cube Visualization
						</h2>
						{cubeStates[currentFrame] && (
							<div className="mt-4 space-y-2">
								<p className="text-xl text-gray-700">
									Iteration: {cubeStates[currentFrame][0]}
								</p>
								<p className="text-xl text-gray-700">
									Score: {cubeStates[currentFrame][2]}
								</p>
								{selectedAlgorithm === "5" && cubeStates[currentFrame][3] !== undefined && (
                                    <p className="text-xl text-gray-700">
                                        Frequency Local: {cubeStates[currentFrame][3]}
                                    </p>
                                )}
							</div>
						)}
					</div>

					<div className="grid grid-cols-1 gap-8">
						{cubeStates[currentFrame]?.[1]?.map((layer, index) =>
							renderCubeLayer(layer, index)
						)}
					</div>

					<div className="flex items-center gap-6">
						<button
							onClick={togglePlayPause}
							className="p-3 rounded-full bg-gradient-to-r from-indigo-500 to-purple-500 text-white hover:from-indigo-600 hover:to-purple-600 transition-all duration-200 transform hover:scale-110"
						>
							{isPlaying ? (
								<Pause className="h-6 w-6" />
							) : (
								<Play className="h-6 w-6" />
							)}
						</button>

						<input
							type="range"
							min="0"
							max={totalFrames - 1}
							value={currentFrame}
							onChange={(e) => setCurrentFrame(Number(e.target.value))}
							className="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
						/>

						<select
							value={playbackSpeed}
							onChange={(e) => setPlaybackSpeed(Number(e.target.value))}
							className="px-4 py-2 rounded-lg bg-gray-50 border border-gray-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition-all appearance-none"
						>
							<option value={0.5}>0.5x</option>
							<option value={1}>1x</option>
							<option value={1.5}>1.5x</option>
							<option value={2}>2x</option>
						</select>

						<button
							onClick={() => setShowPlot(true)}
							className="p-3 rounded-full bg-gradient-to-r from-indigo-500 to-purple-500 text-white hover:from-indigo-600 hover:to-purple-600 transition-all duration-200 transform hover:scale-110"
							title="Show Objective Function Plot"
						>
							<ChartIcon className="h-6 w-6" />
						</button>
					</div>
				</div>
			</div>

			<div className="fixed bottom-8 right-8">
				<div className="bg-white/90 backdrop-blur-md rounded-xl shadow-xl p-4 flex items-center gap-4 border border-white/20">
					<RotateCcw className="h-6 w-6 text-indigo-500" />
					<div>
						<p className="text-sm text-gray-600">Total Time</p>
						<p className="text-2xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
							{totalTime.toFixed(2)}s
						</p>
					</div>
				</div>
			</div>

			{showPlot && renderPlot()}
		</div>
	);
};

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
			) : (
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
