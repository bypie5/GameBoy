import { useEffect, useState } from 'react'

function App() {
  const [wasmModule, setWasmModule] = useState(null)

  useEffect(() => {
    window.Module.onRuntimeInitialized = () => {
      setWasmModule(window.Module)
    }
  })

  const run = () => {
    if (wasmModule) {
      wasmModule._gb_Initialize()
    }
  }

  return (
    <div>
      <h1>Game Boy Color Emulator</h1>
      <button onClick={run}>Run</button>
    </div>
  )
}

export default App
