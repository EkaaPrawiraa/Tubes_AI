import React, { useState, useRef, useEffect } from "react";
import { Pause, Play, Upload } from "lucide-react";
import { Card, CardContent, CardHeader, Typography, Slider, Button, MenuItem, Select, InputLabel, FormControl } from "@mui/material";

const App = () => {
	const [isPlaying, setIsPlaying] = useState(false);
	const [currentFrame, setCurrentFrame] = useState(0);
	const [playbackSpeed, setPlaybackSpeed] = useState(1);
	const [cubeStates, setCubeStates] = useState([]);
	const [totalFrames, setTotalFrames] = useState(0);
	const [totalTime, setTotalTime] = useState(0);
	const animationRef = useRef();

	// Fungsi untuk menangani unggahan file JSON
	const handleFileUpload = (event) => {
		const file = event.target.files[0];
		if (file) {
			const reader = new FileReader();
			reader.onload = (e) => {
				try {
					const data = JSON.parse(e.target.result);
					setCubeStates(data);
					setTotalTime(data);
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

	// Fungsi untuk toggle Play/Pause
	const togglePlayPause = () => {
		setIsPlaying(!isPlaying);
	};

	useEffect(() => {
		if (isPlaying) {
			animationRef.current = requestAnimationFrame(animate);
		} else {
			cancelAnimationFrame(animationRef.current);
		}

		return () => cancelAnimationFrame(animationRef.current);
	}, [isPlaying, currentFrame, playbackSpeed]);

	// Fungsi animasi untuk memainkan frame secara otomatis
	const animate = () => {
		setCurrentFrame((prev) => {
			if (prev >= totalFrames - 1) {
				setIsPlaying(false);
				return prev;
			}
			return prev + 1;
		});
	};

	// Fungsi untuk menampilkan satu layer dari kubus
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
					{/* Menampilkan Iterasi dan Score */}
					{cubeStates[currentFrame] && (
						<div style={{ marginBottom: "16px" }}>
							<Typography variant="h6" color="textPrimary">
								Iteration: {cubeStates[currentFrame][0]}
							</Typography>
							<Typography variant="h6" color="textPrimary">
								Current Score: {cubeStates[currentFrame][1]}
							</Typography>
						</div>
					)}

					{/* Cube Visualization */}
					<div style={{ marginBottom: "32px" }}>
						{cubeStates[currentFrame]?.[2].map((layer, index) => renderCubeLayer(layer, index))}
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
			<div style={{
				position: "fixed",
				bottom: "20px",
				right: "20px",
				backgroundColor: "#fff",
				padding: "10px",
				borderRadius: "8px",
				boxShadow: "0 2px 10px rgba(0,0,0,0.1)",
				zIndex: 1000,
				border: "1px solid #00acc1"
			}}>
				<Typography variant="subtitle1">Total Time:</Typography>
				<Typography variant="h6">{(totalTime / 1000).toFixed(2)} seconds</Typography>
			</div>
		</div>
	);
};

export default App;
