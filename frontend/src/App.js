import React, { useState, useRef, useEffect } from "react";
import { Pause, Play, Upload } from "lucide-react";
import { Card, CardContent, CardHeader, Typography, Slider, Button, MenuItem, Select, InputLabel, FormControl } from "@mui/material";

const App = () => {
	const [isPlaying, setIsPlaying] = useState(false);
	const [currentFrame, setCurrentFrame] = useState(0);
	const [playbackSpeed, setPlaybackSpeed] = useState(1);
	const [cubeStates, setCubeStates] = useState([]);
	const [totalFrames, setTotalFrames] = useState(0);
	const animationRef = useRef();

	// Generate a sample 5x5x5 cube state (replace with actual data loading)
	const generateSampleState = () => {
		const n = 5;
		const cube = Array(n).fill().map(() => Array(n).fill().map(() => Array(n).fill().map(() => Math.floor(Math.random() * (n * n * n) + 1))));
		return cube;
	};

	const handleFileUpload = (event) => {
		const file = event.target.files[0];
		if (file) {
			const reader = new FileReader();
			reader.onload = (e) => {
				try {
					const data = JSON.parse(e.target.result);
					setCubeStates(data);
					setTotalFrames(data.length);
					setCurrentFrame(0);
					setIsPlaying(false);
				} catch (error) {
					console.error("Error parsing file:", error);
				}
			};
			reader.readAsText(file);
		}
	};

	const togglePlayPause = () => {
		setIsPlaying(!isPlaying);
	};

	useEffect(() => {
		const sampleStates = Array(100).fill().map(generateSampleState);
		setCubeStates(sampleStates);
		setTotalFrames(sampleStates.length);
	}, []);

	useEffect(() => {
		if (isPlaying) {
			animationRef.current = requestAnimationFrame(animate);
		} else {
			cancelAnimationFrame(animationRef.current);
		}

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

	const renderCubeLayer = (layer, layerIndex) => {
		if (!cubeStates[currentFrame]) return null;

		return (
			<div style={{ marginBottom: "20px" }}>
				<Typography variant="subtitle2" gutterBottom>Layer {layerIndex + 1}</Typography>
				<div style={{ display: "grid", gridTemplateColumns: "repeat(5, 1fr)", gap: "8px" }}>
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
	};

	return (
		<div style={{ width: "100%", maxWidth: "800px", margin: "auto", padding: "20px" }}>
			<Card>
				<CardHeader title="Magic Cube Visualization" />
				<CardContent>
					{/* Cube Visualization */}
					<div style={{ marginBottom: "32px" }}>
						{cubeStates[currentFrame]?.map((layer, index) => renderCubeLayer(layer, index))}
					</div>

					{/* Controls */}
					<div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
						<Button onClick={togglePlayPause} variant="outlined" color="primary">
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
								onChange={(e) => setPlaybackSpeed(parseFloat(e.target.value))}
								label="Speed"
							>
								<MenuItem value="0.5">0.5x</MenuItem>
								<MenuItem value="1">1x</MenuItem>
								<MenuItem value="2">2x</MenuItem>
								<MenuItem value="4">4x</MenuItem>
							</Select>
						</FormControl>

						<input
							type="file"
							onChange={handleFileUpload}
							style={{ display: "none" }}
							id="file-upload"
							accept=".json"
						/>
						<label htmlFor="file-upload">
							<Button variant="outlined" component="span">
								<Upload />
							</Button>
						</label>
					</div>

					<Typography variant="body2" color="textSecondary" style={{ marginTop: "8px" }}>
						Frame: {currentFrame + 1} / {totalFrames}
					</Typography>
				</CardContent>
			</Card>
		</div>
	);
};

export default App;
