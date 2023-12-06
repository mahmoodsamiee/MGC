import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import Tk, StringVar, ttk, filedialog, messagebox, Frame, Button

def load_data(filepath, combo_box):
    # Read the file, skipping bad lines
    df = pd.read_csv(filepath, header=None, delimiter=',', error_bad_lines=False, warn_bad_lines=True)
    # Keep only rows with exactly 6 columns
    df = df[df.apply(lambda x: len(x) == 6, axis=1)]
    # Rename columns for clarity
    df.columns = ['Operator', 'DateTime', 'WaferID', 'R', 'Resistance', 'Other']

    # Debugging: Print the first few rows of the DataFrame
    print(df.head())

    # Debugging: Print unique WaferID values
    print("Unique Wafer IDs:", df['WaferID'].unique())

    # Update dropdown menu
    wafer_ids = df['WaferID'].unique()
    combo_box['values'] = wafer_ids
    return df


def plot_histogram(wafer_id, data, ax):
    wafer_data = data[data['WaferID'] == wafer_id]

    # Check if there is data for the selected WaferID
    if wafer_data.empty:
        messagebox.showinfo("No Data", f"No data available for Wafer ID: {wafer_id}")
        return

    # Check the contents of wafer_data (you can remove this line later)
    print(wafer_data)

    ax.clear()
    ax.hist(wafer_data['Resistance'], bins=30, edgecolor='black')
    ax.set_title(f'Histogram of Resistance Values for Wafer ID: {wafer_id}')
    ax.set_xlabel('Resistance')
    ax.set_ylabel('Frequency')
    plt.draw()


def save_data(wafer_id, data):
    save_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[("CSV files", "*.csv")], title='Save the resistance values as')
    if save_path:
        wafer_data = data[data['WaferID'] == wafer_id]
        wafer_data.to_csv(save_path, index=False)
        messagebox.showinfo("Success", f"Data saved successfully at {save_path}")

def on_wafer_select(event, combo_box, data, ax):
    wafer_id = combo_box.get()
    plot_histogram(wafer_id, data, ax)

def on_file_open(combo_box, root, ax):
    file_path = filedialog.askopenfilename(title='Select a file to process')
    if file_path:
        global df
        df = load_data(file_path, combo_box)

# Main function
def main():
    root = Tk()
    root.title("Wafer Data Analysis")
    root.geometry("800x600")

    frame = Frame(root)
    frame.pack(pady=20)

    combo_box = ttk.Combobox(frame)
    combo_box.pack(side='left', padx=10)

    open_button = Button(frame, text="Open File", command=lambda: on_file_open(combo_box, root, ax))
    open_button.pack(side='left', padx=10)

    save_button = Button(frame, text="Save Data", command=lambda: save_data(combo_box.get(), df))
    save_button.pack(side='left', padx=10)

    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill='both', expand=True)

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas._tkcanvas.pack()

    combo_box.bind("<<ComboboxSelected>>", lambda event: on_wafer_select(event, combo_box, df, ax))

    root.mainloop()

if __name__ == "__main__":
    main()
