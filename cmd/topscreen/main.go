package main

import (
	"fmt"
	"os/exec"
	"topscreen/internal/adb"
	"topscreen/internal/ui"
)

func main() {
	// Default configuration
	config := adb.Config{
		TapCoords:     [2]int{540, 960},
		SwipeStart:    [2]int{300, 1600},
		SwipeEnd:      [2]int{800, 1600},
		SwipeDuration: 300,
	}

	adbCtrl := adb.NewController(config)

	// Try to start scrcpy
	scrcpyPath, err := exec.LookPath("scrcpy")
	var scrcpyCmd *exec.Cmd
	if err == nil {
		scrcpyCmd = exec.Command(scrcpyPath)
		err := scrcpyCmd.Start()
		if err != nil {
			fmt.Printf("Failed to start scrcpy: %v\n", err)
		} else {
			fmt.Printf("Started scrcpy (pid=%d)\n", scrcpyCmd.Process.Pid)
			defer func() {
				if scrcpyCmd.Process != nil {
					scrcpyCmd.Process.Kill()
				}
			}()
		}
	} else {
		fmt.Println("scrcpy not found in PATH. You can still use the overlay with adb.")
	}

	overlay := ui.NewOverlay(adbCtrl)
	
	// Note: Fyne doesn't have a direct "SetFrameless" in the stable API that works
	// everywhere perfectly without driver specific code, but for now we have a
	// functional window.
	
	overlay.ShowAndRun()
}
