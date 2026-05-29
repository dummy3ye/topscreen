package adb

import (
	"fmt"
	"os/exec"
	"runtime"
	"strings"
)

// Config holds the ADB configuration
type Config struct {
	ADBPath        string
	TapCoords      [2]int
	SwipeStart     [2]int
	SwipeEnd       [2]int
	SwipeDuration  int
}

// Controller handles ADB operations
type Controller struct {
	Config Config
}

// NewController creates a new ADB controller
func NewController(config Config) *Controller {
	if config.ADBPath == "" {
		config.ADBPath = findADB()
	}
	return &Controller{Config: config}
}

func findADB() string {
	path, err := exec.LookPath("adb")
	if err != nil {
		if runtime.GOOS == "windows" {
			return "adb.exe"
		}
		return "adb"
	}
	return path
}

func (c *Controller) run(args ...string) error {
	cmd := exec.Command(c.Config.ADBPath, args...)
	output, err := cmd.CombinedOutput()
	if err != nil {
		return fmt.Errorf("adb error: %v, output: %s", err, string(output))
	}
	return nil
}

// Tap performs a tap at the given coordinates
func (c *Controller) Tap(x, y int) error {
	return c.run("shell", "input", "tap", fmt.Sprintf("%d", x), fmt.Sprintf("%d", y))
}

// Swipe performs a swipe from start to end coordinates
func (c *Controller) Swipe(x1, y1, x2, y2, duration int) error {
	return c.run("shell", "input", "swipe",
		fmt.Sprintf("%d", x1), fmt.Sprintf("%d", y1),
		fmt.Sprintf("%d", x2), fmt.Sprintf("%d", y2),
		fmt.Sprintf("%d", duration))
}

// Back sends the BACK key event
func (c *Controller) Back() error {
	return c.run("shell", "input", "keyevent", "KEYCODE_BACK")
}

// Home sends the HOME key event
func (c *Controller) Home() error {
	return c.run("shell", "input", "keyevent", "KEYCODE_HOME")
}

// Devices returns a list of connected devices
func (c *Controller) Devices() ([]string, error) {
	cmd := exec.Command(c.Config.ADBPath, "devices")
	output, err := cmd.CombinedOutput()
	if err != nil {
		return nil, err
	}

	lines := strings.Split(string(output), "\n")
	var devices []string
	for _, line := range lines[1:] {
		line = strings.TrimSpace(line)
		if line == "" {
			continue
		}
		parts := strings.Fields(line)
		if len(parts) >= 2 && parts[1] == "device" {
			devices = append(devices, parts[0])
		}
	}
	return devices, nil
}
