// This file contains the exported functions for the WebAssembly module.
// These functions are called from JavaScript using the Emscripten-generated JavaScript file.
// See GameBoy/include/GBC.hpp for the function documentation.

#include <GBC.hpp>
#include <emscripten.h>

extern "C"
{

EMSCRIPTEN_KEEPALIVE
void gb_Initialize(uint8_t* frameBuffer, void(*updateScreen)())
{
    Initialize(frameBuffer, updateScreen);
}

EMSCRIPTEN_KEEPALIVE
bool gb_InsertCartridge(char* romPath, char* saveDirectory, char* romName)
{
    return InsertCartridge(romPath, saveDirectory, romName);
}

EMSCRIPTEN_KEEPALIVE
void gb_PowerOn(char* bootRomPath)
{
    PowerOn(bootRomPath);
}

EMSCRIPTEN_KEEPALIVE
void gb_PowerOff()
{
    PowerOff();
}

EMSCRIPTEN_KEEPALIVE
void gb_CollectAudioSamples(float* buffer, int numSamples)
{
    CollectAudioSamples(buffer, numSamples);
}

EMSCRIPTEN_KEEPALIVE
void gb_SetInputs(bool down, bool up, bool left, bool right, bool start, bool select, bool b, bool a)
{
    SetInputs(down, up, left, right, start, select, b, a);
}

EMSCRIPTEN_KEEPALIVE
void gb_SetClockMultiplier(float multiplier)
{
    SetClockMultiplier(multiplier);
}

EMSCRIPTEN_KEEPALIVE
void gb_CreateSaveState(char* saveStatePath)
{
    CreateSaveState(saveStatePath);
}

EMSCRIPTEN_KEEPALIVE
void gb_LoadSaveState(char* saveStatePath)
{
    LoadSaveState(saveStatePath);
}

EMSCRIPTEN_KEEPALIVE
void gb_EnableSoundChannel(int channel, bool enabled)
{
    EnableSoundChannel(channel, enabled);
}

EMSCRIPTEN_KEEPALIVE
void gb_SetMonoAudio(bool monoAudio)
{
    SetMonoAudio(monoAudio);
}

EMSCRIPTEN_KEEPALIVE
void gb_SetVolume(float volume)
{
    SetVolume(volume);
}

EMSCRIPTEN_KEEPALIVE
void gb_SetSampleRate(int sampleRate)
{
    SetSampleRate(sampleRate);
}

EMSCRIPTEN_KEEPALIVE
void gb_PreferDmgColors(bool useDmgColors)
{
    PreferDmgColors(useDmgColors);
}

EMSCRIPTEN_KEEPALIVE
void gb_UseIndividualPalettes(bool individualPalettes)
{
    UseIndividualPalettes(individualPalettes);
}

EMSCRIPTEN_KEEPALIVE
void gb_SetCustomPalette(uint8_t index, uint8_t* data)
{
    SetCustomPalette(index, data);
}
}