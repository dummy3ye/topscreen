package ui

import (
	"image/color"
	"topscreen/internal/adb"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/canvas"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/driver/desktop"
	"fyne.io/fyne/v2/widget"
)

type Overlay struct {
	Window fyne.Window
	adb    *adb.Controller
	config adb.Config
}

func NewOverlay(adbCtrl *adb.Controller) *Overlay {
	a := app.New()
	w := a.NewWindow("topscreen overlay")

	// Set window properties for overlay
	w.SetFixedSize(true)
	w.Resize(fyne.NewSize(220, 150))

	// In Fyne, transparency and frameless are handled via driver-specific hints
	// or by using a custom splash/pop-up window style if supported.
	// For a true overlay, we often need to interact with the underlying driver.
	if drv, ok := fyne.CurrentApp().Driver().(desktop.Driver); ok {
		_ = drv // Placeholder for future desktop-specific tweaks
	}

	o := &Overlay{
		Window: w,
		adb:    adbCtrl,
		config: adbCtrl.Config,
	}

	o.setupUI()
	return o
}

func (o *Overlay) setupUI() {
	// Background for transparency effect (if supported by OS)
	bg := canvas.NewRectangle(color.NRGBA{R: 0, G: 0, B: 0, A: 180})
	bg.SetMinSize(fyne.NewSize(220, 150))

	btnTap := widget.NewButton("Tap", func() {
		o.adb.Tap(o.config.TapCoords[0], o.config.TapCoords[1])
	})

	btnSwipe := widget.NewButton("Swipe", func() {
		o.adb.Swipe(
			o.config.SwipeStart[0], o.config.SwipeStart[1],
			o.config.SwipeEnd[0], o.config.SwipeEnd[1],
			o.config.SwipeDuration,
		)
	})

	btnBack := widget.NewButton("Back", func() {
		o.adb.Back()
	})

	btnHome := widget.NewButton("Home", func() {
		o.adb.Home()
	})

	label := widget.NewLabel("T=Tap, S=Swipe, B=Back, H=Home")
	label.Alignment = fyne.TextAlignCenter

	content := container.NewVBox(
		container.NewGridWithColumns(2, btnTap, btnSwipe),
		container.NewGridWithColumns(2, btnBack, btnHome),
		label,
	)

	// Wrap in a layout that allows dragging if we were frameless
	// For now, use a standard layout
	mainContainer := container.NewMax(bg, container.NewPadded(content))
	o.Window.SetContent(mainContainer)
}

func (o *Overlay) ShowAndRun() {
	o.Window.ShowAndRun()
}
