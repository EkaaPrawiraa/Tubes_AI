import React, { useState, useRef, useEffect } from "react";
import { Pause, Play } from "lucide-react";
import {
	Card,
	CardContent,
	CardHeader,
	Typography,
	Slider,
	Button,
	MenuItem,
	Select,
	InputLabel,
	FormControl,
	CircularProgress,
} from "@mui/material";
import axios from "axios";

const SelectionPage = ({ onSelectAlgorithm }) => {
	const [algorithm, setAlgorithm] = useState("");
	const [maxIteration, setMaxIteration] = useState(100);
	const [population, setPopulation] = useState(100);

	const addedColumn = () => {
		if (algorithm === 2 || algorithm === 3 || algorithm === 6) {
			return (
				<div style={{ padding: "20px", textAlign: "center" }}>
					{algorithm === 6 && (
						<>
							<Typography variant="h4" gutterBottom>
								Total Population
							</Typography>
							<InputLabel>Population</InputLabel>
							<input
								type="number"
								value={population}
								onChange={(e) => setPopulation(Number(e.target.value))}
								placeholder="Input total population number"
								style={{ width: "100%", padding: "8px", marginBottom: "16px" }}
							/>
						</>
					)}
					<Typography variant="h4" gutterBottom>
						MAXIMUM ITERATION
					</Typography>
					<InputLabel>Iteration</InputLabel>
					<input
						type="number"
						value={maxIteration}
						onChange={(e) => setMaxIteration(Number(e.target.value))}
						placeholder="Input max iteration number"
						style={{ width: "100%", padding: "8px", marginBottom: "16px" }}
					/>
				</div>
			);
		}
		return null;
	};

	return (
		<div style={{ padding: "20px", textAlign: "center" }}>
			<Typography variant="h4" gutterBottom>
				Choose Algorithm
			</Typography>
			<FormControl variant="outlined" style={{ minWidth: "200px" }}>
				<InputLabel>Algorithm</InputLabel>
				<Select
					value={algorithm}
					onChange={(e) => setAlgorithm(e.target.value)}
					label="Algorithm"
				>
					<MenuItem value={1}>Steepest Ascent Hill Climbing</MenuItem>
					<MenuItem value={2}>Random Restart Hill Climbing</MenuItem>
					<MenuItem value={3}>Sideways Hill Climbing</MenuItem>
					<MenuItem value={4}>Stochastic Hill Climbing</MenuItem>
					<MenuItem value={5}>Simulated Annealing</MenuItem>
					<MenuItem value={6}>Genetic Algorithm</MenuItem>
				</Select>
			</FormControl>
			<br />
			{addedColumn()}{" "}
			<Button
				variant="contained"
				color="primary"
				style={{ marginTop: "20px" }}
				disabled={!algorithm}
				onClick={() => onSelectAlgorithm(algorithm, maxIteration, population)}
			>
				Start
			</Button>
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
	const animationRef = useRef();

	useEffect(() => {
		const fetchData = async () => {
			setIsLoading(true);
			try {
				let response = [];
				if (selectedAlgorithm === 2 || selectedAlgorithm === 3) {
					response = await axios.post(
						"http://localhost:8000/api/receive-cube/",
						{
							algorithm: selectedAlgorithm,
							max_iteration: maxIteration,
						}
					);
				} else if (selectedAlgorithm === 6) {
					response = await axios.post(
						"http://localhost:8000/api/receive-cube/",
						{
							algorithm: selectedAlgorithm,
							max_iteration: maxIteration,
							population: population,
						}
					);
				} else {
					response = await axios.post(
						"http://localhost:8000/api/receive-cube/",
						{
							algorithm: selectedAlgorithm,
						}
					);
				}

				const data = response.data;
				setCubeStates(data.result);
				setTotalTime(data.total_time);
				setTotalFrames(data.result.length);
				setCurrentFrame(0);
				setIsPlaying(false);
			} catch (error) {
				console.error("Error fetching data:", error);
			} finally {
				setIsLoading(false);
			}
		};
		fetchData();
	}, [selectedAlgorithm, maxIteration, population]);

	const togglePlayPause = () => setIsPlaying(!isPlaying);

	useEffect(() => {
		if (isPlaying) animationRef.current = requestAnimationFrame(animate);
		else cancelAnimationFrame(animationRef.current);

		return () => cancelAnimationFrame(animationRef.current);
	}, [isPlaying, currentFrame, playbackSpeed]);

	const animate = () => {
		setCurrentFrame((prev) => {
			if (prev >= totalFrames - 1) {
				setIsPlaying(false);
				return prev;
			}
			return prev + 1;
		});
	};

	const renderCubeLayer = (layer, layerIndex) => (
		<div key={layerIndex} style={{ marginBottom: "20px" }}>
			<Typography variant="subtitle2" gutterBottom>
				Layer {layerIndex + 1}
			</Typography>
			<div
				style={{
					display: "grid",
					gridTemplateColumns: "repeat(5, 1fr)",
					gap: "8px",
				}}
			>
				{layer.map((row, rowIndex) =>
					row.map((cell, colIndex) => (
						<div
							key={`${layerIndex}-${rowIndex}-${colIndex}`}
							style={{
								width: "40px",
								height: "40px",
								display: "flex",
								alignItems: "center",
								justifyContent: "center",
								backgroundColor: "#e0f7fa",
								border: "1px solid #00acc1",
								borderRadius: "4px",
								fontSize: "14px",
							}}
						>
							{cell}
						</div>
					))
				)}
			</div>
		</div>
	);

	return (
		<div
			style={{
				width: "100%",
				maxWidth: "800px",
				margin: "auto",
				padding: "20px",
			}}
		>
			<Card>
				<CardHeader title="Magic Cube Visualization" />
				<CardContent>
					{isLoading ? (
						<div
							style={{
								display: "flex",
								justifyContent: "center",
								margin: "20px 0",
							}}
						>
							<CircularProgress />
						</div>
					) : (
						<>
							{cubeStates[currentFrame] && (
								<div style={{ marginBottom: "16px" }}>
									<Typography variant="h6" color="textPrimary">
										Iteration: {cubeStates[currentFrame][0]}
									</Typography>
									<Typography variant="h6" color="textPrimary">
										Current Score: {cubeStates[currentFrame][2]}
									</Typography>
								</div>
							)}
							<div style={{ marginBottom: "32px" }}>
								{cubeStates[currentFrame]?.[1]?.map((layer, index) =>
									renderCubeLayer(layer, index)
								)}
							</div>
							<div
								style={{ display: "flex", alignItems: "center", gap: "16px" }}
							>
								<Button
									onClick={togglePlayPause}
									variant="outlined"
									color="primary"
								>
									{isPlaying ? <Pause /> : <Play />}
								</Button>
								<Slider
									value={currentFrame}
									min={0}
									max={totalFrames - 1}
									step={1}
									onChange={(event, value) => setCurrentFrame(value)}
									style={{ flex: 1 }}
								/>
								<FormControl variant="outlined" style={{ width: "100px" }}>
									<InputLabel>Speed</InputLabel>
									<Select
										value={playbackSpeed.toString()}
										onChange={(e) =>
											setPlaybackSpeed(parseFloat(e.target.value))
										}
										label="Speed"
									>
										<MenuItem value="0.5">0.5x</MenuItem>
										<MenuItem value="1">1x</MenuItem>
										<MenuItem value="1.5">1.5x</MenuItem>
										<MenuItem value="2">2x</MenuItem>
									</Select>
								</FormControl>
							</div>
						</>
					)}
				</CardContent>
			</Card>
			<Typography variant="body1" style={{ marginTop: "20px" }}>
				Total time: {totalTime} seconds
			</Typography>
		</div>
	);
};

const App = () => {
	const [step, setStep] = useState(1);
	const [selectedAlgorithm, setSelectedAlgorithm] = useState(null);
	const [maxIteration, setMaxIteration] = useState(100);
	const [population, setPopulation] = useState(100);

	const handleSelectAlgorithm = (algorithm, max_iteration, populations) => {
		console.log(algorithm, max_iteration, populations);
		setSelectedAlgorithm(algorithm);
		setMaxIteration(max_iteration);
		setPopulation(populations);
		setStep(2);
	};

	return (
		<div>
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
