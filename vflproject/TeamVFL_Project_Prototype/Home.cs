using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using static System.Windows.Forms.VisualStyles.VisualStyleElement;
using Python.Runtime;
using Newtonsoft.Json;
using OxyPlot;
using OxyPlot.Series;
using OxyPlot.WindowsForms;
using OxyPlot.Axes;
using OxyPlot.Annotations;
using System.Runtime.Remoting.Messaging;
using System.Reflection;
using OxyPlot.Wpf;


namespace TeamVFL_Project_Prototype
{
    public partial class Home : Form
    {
        private PlotModel plotModel;
        private LineSeries s11Series;
        private LineSeries s12Series;
        private LineSeries s21Series;
        private LineSeries s22Series;
        public dynamic PyLauncher;
        private string selectedFilePath;
        private bool Optimized;
        private string cleanedJson;
        private System.Timers.Timer timer;
        private int remainingTime = 20;


        public Home()
        {
            InitializeComponent();
            contourPlot.Model = CreatePlotModel();
            // Define paths
            string basePath = Path.Combine(Directory.GetCurrentDirectory());
            string hflibPath = Path.Combine(Directory.GetCurrentDirectory(), @"hflib");
            string python39 = Path.Combine(Directory.GetCurrentDirectory(), @"common\python39\python39.dll");
            string modulePath = Path.Combine(Directory.GetCurrentDirectory(), @"common\pythonlib");
            string envPath = Path.Combine(Directory.GetCurrentDirectory(), @"common\python39");
            string oriPath = Environment.GetEnvironmentVariable("PATH")?.TrimEnd(Path.PathSeparator);
            oriPath = string.IsNullOrEmpty(oriPath) ? envPath : oriPath + Path.PathSeparator + envPath;

            // Set Environment Variables
            Environment.SetEnvironmentVariable("PATH", oriPath, EnvironmentVariableTarget.Process);
            Environment.SetEnvironmentVariable("PYTHONNET_PYDLL", python39);
            Environment.SetEnvironmentVariable("PYTHONPATH", $"{modulePath}{Path.PathSeparator}{basePath}{Path.PathSeparator}{hflibPath}", EnvironmentVariableTarget.Process);

            // Initialize Python Engine
            PythonEngine.PythonPath = PythonEngine.PythonPath + Path.PathSeparator + Environment.GetEnvironmentVariable("PYTHONPATH", EnvironmentVariableTarget.Process);
            PythonEngine.Initialize();

            // Initialize the launcher, first import launch.pyd, then initialize its class constructor
            using (Py.GIL())
            {
                dynamic launcher = Py.Import("launch");
                PyLauncher = launcher.HFLaunch();
            }
            Optimized = false;
            cleanedJson = null;

            // Set initial checkbox states
            checkboxS11.Checked = true;
            checkboxS12.Checked = true;

            checkboxS11.CheckedChanged += CheckboxS11_CheckedChanged;
            checkboxS12.CheckedChanged += CheckboxS12_CheckedChanged;
            checkboxS21.CheckedChanged += CheckboxS21_CheckedChanged;
            checkboxS22.CheckedChanged += CheckboxS22_CheckedChanged;

            g0_Response.SelectedIndex = 0;
            g1_Response.SelectedIndex = 0;
            g2_Response.SelectedIndex = 0;

            g0_Series.SelectedIndex = 0;
            g1_Series.SelectedIndex = 2;
            g2_Series.SelectedIndex = 2;

            g0_Value.Text = "-15";
            g1_Value.Text = "-15";
            g2_Value.Text = "-15";

            g0_Min.Text = "0.1";
            g1_Min.Text = "0.01";
            g2_Min.Text = "0.554";

            g0_Max.Text = "0.45";
            g1_Max.Text = "0.079";
            g2_Max.Text = "1.0";

            g0_Value.TextChanged += G0_Parameters_TextChanged;
            g0_Min.TextChanged += G0_Parameters_TextChanged;
            g0_Max.TextChanged += G0_Parameters_TextChanged;

            g1_Value.TextChanged += G1_Parameters_TextChanged;
            g1_Min.TextChanged += G1_Parameters_TextChanged;
            g1_Max.TextChanged += G1_Parameters_TextChanged;

            g2_Value.TextChanged += G2_Parameters_TextChanged;
            g2_Min.TextChanged += G2_Parameters_TextChanged;
            g2_Max.TextChanged += G2_Parameters_TextChanged;

            c1_Min.Text = "10";
            l1_Min.Text = "10";
            c2_Min.Text = "10";
            l2_Min.Text = "10";
            c3_Min.Text = "10";
            l3_Min.Text = "10";

            c1_Max.Text = "100";
            l1_Max.Text = "100";
            c2_Max.Text = "100";
            l2_Max.Text = "100";
            c3_Max.Text = "100";
            l3_Max.Text = "100";
        }

        
        /*
        private void RunPythonScriptButton_Click(object sender, EventArgs e)
        {
            PyObject output = null;

            // Use this block Py.GIL() to lock, it waits backends Python to finish execution
            using (Py.GIL())
            {
                output = PyLauncher.load_design(@"C:\Users\leongsheng\source\repos\vflproject\pythonAPI\BPF-4-100M-450M.fpx");
            }

            string dummy = "";
            outputTextBox.Text = output.ToString();
        }*/

        private void ProcessFileAndGenerateChart()
        {
            c1_Optimize.Checked = true;
            c2_Optimize.Checked = true;
            c3_Optimize.Checked = true;
            l1_Optimize.Checked = true;
            l2_Optimize.Checked = true;
            l3_Optimize.Checked = true;
            Optimized = false;

            PyObject output = null;

            using (Py.GIL())
            {
                output = PyLauncher.load_design(selectedFilePath);
            }
            //outputTextBox.Text = output.ToString();

            file_path.Text = selectedFilePath;
            Console.WriteLine(output.ToString());
            // Change python json output to dynamic object
            dynamic jsonResponse = JsonConvert.DeserializeObject(output.ToString());

            // Get S11 Data
            dynamic s11Data = jsonResponse.SimulationResult.Response1.Series.Series1;
            double[] s11DataX = s11Data.DataX.ToObject<double[]>();
            double[] s11DataY = s11Data.DataY.ToObject<double[]>();

            // Get S12 Data
            dynamic s12Data = jsonResponse.SimulationResult.Response1.Series.Series2;
            double[] s12DataX = s12Data.DataX.ToObject<double[]>();
            double[] s12DataY = s12Data.DataY.ToObject<double[]>();

            // Get S21 Data
            dynamic s21Data = jsonResponse.SimulationResult.Response1.Series.Series3;
            double[] s21DataX = s21Data.DataX.ToObject<double[]>();
            double[] s21DataY = s21Data.DataY.ToObject<double[]>();

            // Get S22 Data
            dynamic s22Data = jsonResponse.SimulationResult.Response1.Series.Series4;
            double[] s22DataX = s22Data.DataX.ToObject<double[]>();
            double[] s22DataY = s22Data.DataY.ToObject<double[]>();

            // Accessing component values
            dynamic components = jsonResponse.Components;
            foreach (var component in components)
            {
                switch (component.Name.ToString())
                {
                    case "c1":
                        double c1Value = component.Value;
                        c1_value.Text = c1Value.ToString(); // Assuming textboxC1 is the TextBox for c1
                        break;
                    case "l1":
                        double l1Value = component.Value;
                        l1_value.Text = l1Value.ToString(); // Assuming textboxL1 is the TextBox for l1
                        break;
                    case "c2":
                        double c2Value = component.Value;
                        c2_value.Text = c2Value.ToString(); // Assuming textboxC2 is the TextBox for c2
                        break;
                    case "l2":
                        double l2Value = component.Value;
                        l2_value.Text = l2Value.ToString(); // Assuming textboxL2 is the TextBox for l2
                        break;
                    case "c3":
                        double c3Value = component.Value;
                        c3_value.Text = c3Value.ToString(); // Assuming textboxC3 is the TextBox for c3
                        break;
                    case "l3":
                        double l3Value = component.Value;
                        l3_value.Text = l3Value.ToString(); // Assuming textboxL3 is the TextBox for l3
                        break;
                    default:
                        // Handle other components if needed
                        break;
                }
            }


            // Create OxyPlot chart
            plotModel = new PlotModel { Title = "S-Parameters" };

            s11Series = CreateLineSeries(s11DataX, s11DataY, OxyColor.FromRgb(0, 0, 255));
            s12Series = CreateLineSeries(s12DataX, s12DataY, OxyColor.FromRgb(255, 0, 0));
            s21Series = CreateLineSeries(s21DataX, s21DataY, OxyColor.FromRgb(0, 255, 0));
            s22Series = CreateLineSeries(s22DataX, s22DataY, OxyColor.FromRgb(255, 255, 0));

            ToggleSeriesVisibility(s11Series, checkboxS11.Checked);
            ToggleSeriesVisibility(s12Series, checkboxS12.Checked);
            ToggleSeriesVisibility(s21Series, checkboxS21.Checked);
            ToggleSeriesVisibility(s22Series, checkboxS22.Checked);
            plotModel.Axes.Clear();
            plotModel.Axes.Add(new OxyPlot.Axes.LinearAxis
            {
                Position = OxyPlot.Axes.AxisPosition.Bottom,
                Title = "Frequency",
                Unit = "GHz",
                MajorGridlineStyle = LineStyle.Solid,
                MinorGridlineStyle = LineStyle.Dot,
                Key = "FrequencyAxis"
            });
            plotModel.Axes.Add(new OxyPlot.Axes.LinearAxis
            {
                Position = AxisPosition.Left,
                MajorGridlineStyle = LineStyle.Solid,
                MinorGridlineStyle = LineStyle.Dot,
                Title = "dB"
            });

            var g0Line = new LineAnnotation
            {
                Type = LineAnnotationType.Horizontal,
                Y = Convert.ToDouble(g0_Value.Text),
                Color = OxyColor.FromRgb(0, 255, 0),
                LineStyle = LineStyle.DashDot
            };
            g0Line.MinimumX = Convert.ToDouble(g0_Min.Text);
            g0Line.MaximumX = Convert.ToDouble(g0_Max.Text);
            plotModel.Annotations.Add(g0Line);


            var g0Label = new TextAnnotation
            {
                Text = "g0",
                TextPosition = new DataPoint((g0Line.MinimumX + g0Line.MaximumX) / 2, g0Line.Y),
                TextVerticalAlignment = VerticalAlignment.Bottom,
                TextHorizontalAlignment = OxyPlot.HorizontalAlignment.Center,
                TextColor = OxyColor.FromRgb(0, 255, 0),
                StrokeThickness = 0
            };
            plotModel.Annotations.Add(g0Label);


            var g1Line = new LineAnnotation
            {
                Type = LineAnnotationType.Horizontal,
                Y = Convert.ToDouble(g1_Value.Text),
                Color = OxyColor.FromRgb(255, 0, 0),
                LineStyle = LineStyle.DashDot
            };
            g1Line.MinimumX = Convert.ToDouble(g1_Min.Text);
            g1Line.MaximumX = Convert.ToDouble(g1_Max.Text);
            plotModel.Annotations.Add(g1Line);
            var g1Label = new TextAnnotation
            {
                Text = "g1",
                TextPosition = new DataPoint((g1Line.MinimumX + g1Line.MaximumX) / 2, g1Line.Y),
                TextVerticalAlignment = VerticalAlignment.Bottom,
                TextHorizontalAlignment = OxyPlot.HorizontalAlignment.Center,
                TextColor = OxyColor.FromRgb(255, 0, 0),
                StrokeThickness = 0
            };
            plotModel.Annotations.Add(g1Label);


            var g2Line = new LineAnnotation
            {
                Type = LineAnnotationType.Horizontal,
                Y = Convert.ToDouble(g2_Value.Text),
                Color = OxyColor.FromRgb(255, 0, 0),
                LineStyle = LineStyle.DashDot
            };
            g2Line.MinimumX = Convert.ToDouble(g2_Min.Text);
            g2Line.MaximumX = Convert.ToDouble(g2_Max.Text);
            plotModel.Annotations.Add(g2Line);

            var g2Label = new TextAnnotation
            {
                Text = "g2",
                TextPosition = new DataPoint((g2Line.MinimumX + g2Line.MaximumX) / 2, g2Line.Y),
                TextVerticalAlignment = VerticalAlignment.Bottom,
                TextHorizontalAlignment = OxyPlot.HorizontalAlignment.Center,
                TextColor = OxyColor.FromRgb(255, 0, 0),
                StrokeThickness = 0
            };
            plotModel.Annotations.Add(g2Label);

            // Clear previous content in plotPanel
            plotPanel.Controls.Clear();

            // Create a PlotView to display the plot model
            var plotView = new OxyPlot.WindowsForms.PlotView
            {
                Model = plotModel,
                Dock = DockStyle.Fill // Dock the plotView to fill the form
            };

            // Add the PlotView to your form (assuming you have a panel named plotPanel)
            plotPanel.Controls.Add(plotView);
        }

        private void ShowGraph_Click(object sender, EventArgs e)
        {
            OpenFileDialog openFileDialog = new OpenFileDialog();
            openFileDialog.Title = "Select File";
            openFileDialog.Filter = "FPX Files (*.fpx)|*.fpx";

            if (openFileDialog.ShowDialog() == DialogResult.OK)
            {
                if (Path.GetExtension(openFileDialog.FileName).ToLower() == ".fpx")
                {
                    selectedFilePath = openFileDialog.FileName;
                    ProcessFileAndGenerateChart();
                }
                else
                {
                    MessageBox.Show("Please select a .fpx file.", "Invalid File Type", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }
            }

        }

        private LineSeries CreateLineSeries(double[] dataX, double[] dataY, OxyColor color)
        {
            var series = new LineSeries { Color = color };

            for (int i = 0; i < dataX.Length; i++)
            {
                // Assuming dataX is in frequency (Hz)
                series.Points.Add(new DataPoint(dataX[i] / 1e9, dataY[i]));
            }

            return series;
        }

        private void ToggleSeriesVisibility(LineSeries series, bool isVisible)
        {
            if (isVisible && !plotModel.Series.Contains(series))
            {
                plotModel.Series.Add(series);
            }
            else if (!isVisible && plotModel.Series.Contains(series))
            {
                plotModel.Series.Remove(series);
            }

            plotPanel.Invalidate();
        }

        private void CheckboxS11_CheckedChanged(object sender, EventArgs e)
        {
            if (!string.IsNullOrEmpty(selectedFilePath) && Optimized==false) 
            {
                ProcessFileAndGenerateChart(); 
            }
            else if (Optimized == true)
            {
                ProcessJsonResponse(cleanedJson);
            }
        }

        private void CheckboxS12_CheckedChanged(object sender, EventArgs e)
        {
            if (!string.IsNullOrEmpty(selectedFilePath) && Optimized == false)
            {
                ProcessFileAndGenerateChart();
            }
            else if (Optimized == true)
            {
                ProcessJsonResponse(cleanedJson);
            }
        }

        private void CheckboxS21_CheckedChanged(object sender, EventArgs e)
        {
            if (!string.IsNullOrEmpty(selectedFilePath) && Optimized == false)
            {
                ProcessFileAndGenerateChart();
            }
            else if (Optimized == true)
            {
                ProcessJsonResponse(cleanedJson);
            }
        }

        private void CheckboxS22_CheckedChanged(object sender, EventArgs e)
        {
            if (!string.IsNullOrEmpty(selectedFilePath) && Optimized == false)
            {
                ProcessFileAndGenerateChart();
            }
            else if (Optimized == true)
            {
                ProcessJsonResponse(cleanedJson);
            }
        }

        private void G0_Parameters_TextChanged(object sender, EventArgs e)
        {
            if (!string.IsNullOrEmpty(selectedFilePath))
            {
                // Check if each text is a valid double
                bool isG0ValueValid = double.TryParse(g0_Value.Text, out double g0Value);
                bool isG0MinValid = double.TryParse(g0_Min.Text, out double g0Min);
                bool isG0MaxValid = double.TryParse(g0_Max.Text, out double g0Max);

                if (isG0ValueValid && isG0MinValid && isG0MaxValid)
                {
                    // Perform chart generation if all inputs are valid
                    ProcessFileAndGenerateChart();
                }
                else
                {
                    // Reset only the invalid inputs
                    if (!isG0ValueValid)
                    {
                        g0_Value.Text = "-"; // Or any other default value for g0_Value
                    }

                    if (!isG0MinValid)
                    {
                        g0_Min.Text = "0.1"; // Or any other default value for g0_Min
                    }

                    if (!isG0MaxValid)
                    {
                        g0_Max.Text = "0.45"; // Or any other default value for g0_Max
                    }
                }
            }
        }
        private void G1_Parameters_TextChanged(object sender, EventArgs e)
        {
            if (!string.IsNullOrEmpty(selectedFilePath))
            {
                // Check if each text is a valid double
                bool isG1ValueValid = double.TryParse(g1_Value.Text, out double g1Value);
                bool isG1MinValid = double.TryParse(g1_Min.Text, out double g1Min);
                bool isG1MaxValid = double.TryParse(g1_Max.Text, out double g1Max);

                if (isG1ValueValid && isG1MinValid && isG1MaxValid)
                {
                    // Perform chart generation if all inputs are valid
                    ProcessFileAndGenerateChart();
                }
                else
                {

                    // Reset only the invalid inputs
                    if (!isG1ValueValid)
                    {
                        g1_Value.Text = "-"; 
                    }

                    if (!isG1MinValid)
                    {
                        g1_Min.Text = "0.01"; 
                    }

                    if (!isG1MaxValid)
                    {
                        g1_Max.Text = "0.079"; 
                    }
                }
            }
        }
        private void G2_Parameters_TextChanged(object sender, EventArgs e)
        {
            if (!string.IsNullOrEmpty(selectedFilePath))
            {
                // Check if each text is a valid double
                bool isG2ValueValid = double.TryParse(g2_Value.Text, out double g2Value);
                bool isG2MinValid = double.TryParse(g2_Min.Text, out double g2Min);
                bool isG2MaxValid = double.TryParse(g2_Max.Text, out double g2Max);

                if (isG2ValueValid && isG2MinValid && isG2MaxValid)
                {
                    // Perform chart generation if all inputs are valid
                    ProcessFileAndGenerateChart();
                }
                else
                {

                    // Reset only the invalid inputs
                    if (!isG2ValueValid)
                    {
                        g2_Value.Text = "-"; 
                    }

                    if (!isG2MinValid)
                    {
                        g2_Min.Text = "0.554"; 
                    }

                    if (!isG2MaxValid)
                    {
                        g2_Max.Text = "1.0"; 
                    }
                }
            }
        }

        private void btn_optimize_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrEmpty(selectedFilePath))
            {
                MessageBox.Show("Please Import File First");
            }
            else
            {
                float c1v = float.Parse(c1_value.Text);
                float c1_min = float.Parse(c1_Min.Text);
                float c1_max = float.Parse(c1_Max.Text);

                float l1v = float.Parse(l1_value.Text);
                float l1_min = float.Parse(l1_Min.Text);
                float l1_max = float.Parse(l1_Max.Text);

                float c2v = float.Parse(c2_value.Text);
                float c2_min = float.Parse(c2_Min.Text);
                float c2_max = float.Parse(c2_Max.Text);

                float l2v = float.Parse(l2_value.Text);
                float l2_min = float.Parse(l2_Min.Text);
                float l2_max = float.Parse(l2_Max.Text);

                float c3v = float.Parse(c3_value.Text);
                float c3_min = float.Parse(c3_Min.Text);
                float c3_max = float.Parse(c3_Max.Text);

                float l3v = float.Parse(l3_value.Text);
                float l3_min = float.Parse(l3_Min.Text);
                float l3_max = float.Parse(l3_Max.Text);
                if (c1v < c1_min || c1v > c1_max)
                {
                    MessageBox.Show("Please ensure c1 value between Min and Max");
                }
                else if (l1v < l1_min || l1v > l1_max)
                {
                    MessageBox.Show("Please ensure l1 value between Min and Max");
                }
                else if (c2v < c2_min || c2v > c2_max)
                {
                    MessageBox.Show("Please ensure c2 value between Min and Max");
                }
                else if (l2v < l2_min || l2v > l2_max)
                {
                    MessageBox.Show("Please ensure l2 value between Min and Max");
                }
                else if (c3v < c3_min || c3v > c3_max)
                {
                    MessageBox.Show("Please ensure c3 value between Min and Max");
                }
                else if (l3v < l3_min || l3v > l3_max)
                {
                    MessageBox.Show("Please ensure l3 value between Min and Max");
                }
                else
                {
                    string currentFilePath = Assembly.GetExecutingAssembly().Location;
                    Console.WriteLine("Current File Path: " + currentFilePath);
                    DirectoryInfo currentDirectory = new DirectoryInfo(Path.GetDirectoryName(currentFilePath));
                    DirectoryInfo projectDirectory = currentDirectory.Parent.Parent.Parent.Parent;
                    Console.WriteLine("Project Directory Path: " + projectDirectory.FullName);
                    string relativePath = @"pythonAPI\vfl_marl_version1.0\RunAfterTraining_Desktop.py";
                    string pythonFilePath = Path.Combine(projectDirectory.FullName, relativePath);

                    if (File.Exists(pythonFilePath) && !string.IsNullOrEmpty(selectedFilePath))
                    {
                        Optimize_output.Clear();
                        Optimize_output.AppendText("Optimizing.... estimate time 20~40 seconds\n");
                        string c1 = c1_value.Text;
                        string l1 = l1_value.Text;
                        string c2 = c2_value.Text;
                        string l2 = l2_value.Text;
                        string c3 = c3_value.Text;
                        string l3 = l3_value.Text;
                        string c1_O_min = c1_Min.Text;
                        string c1_O_max = c1_Max.Text;
                        string l1_O_min = l1_Min.Text;
                        string l1_O_max = l1_Max.Text;
                        string c2_O_min = c2_Min.Text;
                        string c2_O_max = c2_Max.Text;
                        string l2_O_min = l2_Min.Text;
                        string l2_O_max = l2_Max.Text;
                        string c3_O_min = c3_Min.Text;
                        string c3_O_max = c3_Max.Text;
                        string l3_O_min = l3_Min.Text;
                        string l3_O_max = l3_Max.Text;
                        string g0_s = g0_Series.Text;
                        string g1_s = g1_Series.Text;
                        string g2_s = g2_Series.Text;
                        string g0_v = g0_Value.Text;
                        string g1_v = g1_Value.Text;
                        string g2_v = g2_Value.Text;
                        string g0_mi = g0_Min.Text + "e9";
                        string g0_ma = g0_Max.Text + "e9";
                        string g1_mi = g1_Min.Text + "e9";
                        string g1_ma = g1_Max.Text + "e9";
                        string g2_mi = g2_Min.Text + "e9";
                        string g2_ma = g2_Max.Text + "e9";

                        string arguments = $"{c1} {l1} {c2} {l2} {c3} {l3} {c1_O_min} {c1_O_max} {l1_O_min} {l1_O_max} {c2_O_min} {c2_O_max} {l2_O_min} {l2_O_max} {c3_O_min} {c3_O_max} {l3_O_min} {l3_O_max}" +
                            $" {g0_s} {g1_s} {g2_s} {g0_v} {g1_v} {g2_v} {g0_mi} {g0_ma} {g1_mi} {g1_ma} {g2_mi} {g2_ma}";

                        string pythonCommand = $"\"{pythonFilePath}\" {arguments}";

                        Task.Run(() =>
                        {
                            string output = ExecutePythonScript(pythonCommand, arguments);
                            if (Optimize_output.InvokeRequired)
                            {
                                Optimize_output.Invoke(new Action(() => Optimize_output.AppendText(output)));
                            }
                            else
                            {
                                Optimize_output.AppendText(output);
                            }

                            string[] lines = output.Split('\n');
                            string bestParameters = "";
                            foreach (string line in lines)
                            {
                                if (line.Contains("Current Step: 60"))
                                {
                                    bestParameters = line.Split('|')[3].Trim().Split(':')[1].Trim();
                                    break;
                                }
                            }

                            Console.WriteLine($"Best Parameters at step 60: {bestParameters}");
                            if (Optimize_output.InvokeRequired)
                            {
                                Optimize_output.Invoke(new Action(() => UpdateGraph(bestParameters)));
                            }
                            else
                            {
                                UpdateGraph(bestParameters);
                            }
                        });

                    }
                }
            }
            
        }

        private void UpdateGraph(string bestParameters)
        {
            string currentFilePath = Assembly.GetExecutingAssembly().Location;
            Console.WriteLine("Current File Path: " + currentFilePath);

            DirectoryInfo currentDirectory = new DirectoryInfo(Path.GetDirectoryName(currentFilePath));
            DirectoryInfo projectDirectory = currentDirectory.Parent.Parent.Parent.Parent;
            Console.WriteLine("Project Directory Path: " + projectDirectory.FullName);

            string relativePath = @"pythonAPI\vfl_marl_version1.0\update_graph.py";
            string updateGraphScriptPath = Path.Combine(projectDirectory.FullName, relativePath);

            if (File.Exists(updateGraphScriptPath))
            {
                // Split the bestParameters string into individual values
                string[] parametersArray = bestParameters.Replace("[", "").Replace("]", "").Split(',');

                // Trim and convert each parameter to string
                for (int i = 0; i < parametersArray.Length; i++)
                {
                    parametersArray[i] = parametersArray[i].Trim();
                }
                // Construct the arguments string with individual parameters
                string pythonPath = Path.Combine(projectDirectory.FullName, @"TeamVFL_Project_Prototype\bin\x64\Release\common\python39\python.exe");
                string scriptPath = $"\"{updateGraphScriptPath}\"";
                string arguments = $"{parametersArray[0]} {parametersArray[1]} {parametersArray[2]} {parametersArray[3]} {parametersArray[4]} {parametersArray[5]}";
                PyObject output = ExecutePythonScriptObject(scriptPath, arguments);
                Console.WriteLine(output.ToString());
                cleanedJson = output.ToString().Replace("None", "null").Replace("True", "true"); ;
                Console.WriteLine(cleanedJson);
                // Accessing component values
                c1_value.Text = parametersArray[0].ToString();
                l1_value.Text = parametersArray[1].ToString();
                c2_value.Text = parametersArray[2].ToString();
                l2_value.Text = parametersArray[3].ToString();
                c3_value.Text = parametersArray[4].ToString();
                l3_value.Text = parametersArray[5].ToString();
                ProcessJsonResponse(cleanedJson);
                Optimized = true;

            }
            else
            {
                Console.WriteLine("update_graph.py not found!");
            }
        }

        private string ExecutePythonScript(string scriptName, string arguments)
        {
            string currentFilePath = Assembly.GetExecutingAssembly().Location;
            Console.WriteLine("Current File Path: " + currentFilePath);
            DirectoryInfo currentDirectory = new DirectoryInfo(Path.GetDirectoryName(currentFilePath));
            DirectoryInfo projectDirectory = currentDirectory.Parent.Parent.Parent.Parent;
            Console.WriteLine("Project Directory Path: " + projectDirectory.FullName);
            string relativePath = @"TeamVFL_Project_Prototype\bin\x64\Release\common\python39\python.exe";
            ProcessStartInfo startInfo = new ProcessStartInfo
            {
                FileName = Path.Combine(projectDirectory.FullName, relativePath),
                Arguments = $"{scriptName} {arguments}",
                UseShellExecute = false,
                RedirectStandardOutput = true,
                CreateNoWindow = true
            };

            using (Process process = Process.Start(startInfo))
            {
                using (StreamReader reader = process.StandardOutput)
                {
                    string result = reader.ReadToEnd();
                    process.WaitForExit();
                    return result;
                }
            }
        }

        private PyObject ExecutePythonScriptObject(string scriptName, string arguments)
        {
            string currentFilePath = Assembly.GetExecutingAssembly().Location;
            Console.WriteLine("Current File Path: " + currentFilePath);
            DirectoryInfo currentDirectory = new DirectoryInfo(Path.GetDirectoryName(currentFilePath));
            DirectoryInfo projectDirectory = currentDirectory.Parent.Parent.Parent.Parent;
            Console.WriteLine("Project Directory Path: " + projectDirectory.FullName);
            string relativePath = @"TeamVFL_Project_Prototype\bin\x64\Release\common\python39\python.exe";
            ProcessStartInfo startInfo = new ProcessStartInfo
            {
                FileName = Path.Combine(projectDirectory.FullName, relativePath),
                Arguments = $"{scriptName} {arguments}",
                UseShellExecute = false,
                RedirectStandardOutput = true,
                CreateNoWindow = true
            };

            using (Process process = Process.Start(startInfo))
            {
                using (StreamReader reader = process.StandardOutput)
                {
                    dynamic result = reader.ReadToEnd();
                    process.WaitForExit();
                    // Return a PyObject instead of a string
                    return new PyString(result);
                }
            }
        }

        private void ProcessJsonResponse(string jsonResponseString)
        {
            // Change python json output to dynamic object
            dynamic jsonResponse = JsonConvert.DeserializeObject(jsonResponseString, new JsonSerializerSettings
            {
                FloatParseHandling = FloatParseHandling.Double,
                NullValueHandling = NullValueHandling.Ignore
            });

            // Get S11 Data
            dynamic s11Data = jsonResponse.SimulationResult.Response1.Series.Series1;
            double[] s11DataX = s11Data.DataX.ToObject<double[]>();
            double[] s11DataY = s11Data.DataY.ToObject<double[]>();

            // Get S12 Data
            dynamic s12Data = jsonResponse.SimulationResult.Response1.Series.Series2;
            double[] s12DataX = s12Data.DataX.ToObject<double[]>();
            double[] s12DataY = s12Data.DataY.ToObject<double[]>();

            // Get S21 Data
            dynamic s21Data = jsonResponse.SimulationResult.Response1.Series.Series3;
            double[] s21DataX = s21Data.DataX.ToObject<double[]>();
            double[] s21DataY = s21Data.DataY.ToObject<double[]>();

            // Get S22 Data
            dynamic s22Data = jsonResponse.SimulationResult.Response1.Series.Series4;
            double[] s22DataX = s22Data.DataX.ToObject<double[]>();
            double[] s22DataY = s22Data.DataY.ToObject<double[]>();

            // Create OxyPlot chart
            plotModel = new PlotModel { Title = "S-Parameters" };

            s11Series = CreateLineSeries(s11DataX, s11DataY, OxyColor.FromRgb(0, 0, 255));
            s12Series = CreateLineSeries(s12DataX, s12DataY, OxyColor.FromRgb(255, 0, 0));
            s21Series = CreateLineSeries(s21DataX, s21DataY, OxyColor.FromRgb(0, 255, 0));
            s22Series = CreateLineSeries(s22DataX, s22DataY, OxyColor.FromRgb(255, 255, 0));

            ToggleSeriesVisibility(s11Series, checkboxS11.Checked);
            ToggleSeriesVisibility(s12Series, checkboxS12.Checked);
            ToggleSeriesVisibility(s21Series, checkboxS21.Checked);
            ToggleSeriesVisibility(s22Series, checkboxS22.Checked);
            plotModel.Axes.Clear();
            plotModel.Axes.Add(new OxyPlot.Axes.LinearAxis
            {
                Position = OxyPlot.Axes.AxisPosition.Bottom,
                Title = "Frequency",
                Unit = "GHz",
                MajorGridlineStyle = LineStyle.Solid,
                MinorGridlineStyle = LineStyle.Dot,
                Key = "FrequencyAxis"
            });
            plotModel.Axes.Add(new OxyPlot.Axes.LinearAxis
            {
                Position = AxisPosition.Left,
                MajorGridlineStyle = LineStyle.Solid,
                MinorGridlineStyle = LineStyle.Dot,
                Title = "dB"
            });

            var g0Line = new LineAnnotation
            {
                Type = LineAnnotationType.Horizontal,
                Y = Convert.ToDouble(g0_Value.Text),
                Color = OxyColor.FromRgb(0, 255, 0),
                LineStyle = LineStyle.DashDot
            };
            g0Line.MinimumX = Convert.ToDouble(g0_Min.Text);
            g0Line.MaximumX = Convert.ToDouble(g0_Max.Text);
            plotModel.Annotations.Add(g0Line);


            var g0Label = new TextAnnotation
            {
                Text = "g0",
                TextPosition = new DataPoint((g0Line.MinimumX + g0Line.MaximumX) / 2, g0Line.Y),
                TextVerticalAlignment = VerticalAlignment.Bottom,
                TextHorizontalAlignment = OxyPlot.HorizontalAlignment.Center,
                TextColor = OxyColor.FromRgb(0, 255, 0),
                StrokeThickness = 0
            };
            plotModel.Annotations.Add(g0Label);


            var g1Line = new LineAnnotation
            {
                Type = LineAnnotationType.Horizontal,
                Y = Convert.ToDouble(g1_Value.Text),
                Color = OxyColor.FromRgb(255, 0, 0),
                LineStyle = LineStyle.DashDot
            };
            g1Line.MinimumX = Convert.ToDouble(g1_Min.Text);
            g1Line.MaximumX = Convert.ToDouble(g1_Max.Text);
            plotModel.Annotations.Add(g1Line);
            var g1Label = new TextAnnotation
            {
                Text = "g1",
                TextPosition = new DataPoint((g1Line.MinimumX + g1Line.MaximumX) / 2, g1Line.Y),
                TextVerticalAlignment = VerticalAlignment.Bottom,
                TextHorizontalAlignment = OxyPlot.HorizontalAlignment.Center,
                TextColor = OxyColor.FromRgb(255, 0, 0),
                StrokeThickness = 0
            };
            plotModel.Annotations.Add(g1Label);


            var g2Line = new LineAnnotation
            {
                Type = LineAnnotationType.Horizontal,
                Y = Convert.ToDouble(g2_Value.Text),
                Color = OxyColor.FromRgb(255, 0, 0),
                LineStyle = LineStyle.DashDot
            };
            g2Line.MinimumX = Convert.ToDouble(g2_Min.Text);
            g2Line.MaximumX = Convert.ToDouble(g2_Max.Text);
            plotModel.Annotations.Add(g2Line);

            var g2Label = new TextAnnotation
            {
                Text = "g2",
                TextPosition = new DataPoint((g2Line.MinimumX + g2Line.MaximumX) / 2, g2Line.Y),
                TextVerticalAlignment = VerticalAlignment.Bottom,
                TextHorizontalAlignment = OxyPlot.HorizontalAlignment.Center,
                TextColor = OxyColor.FromRgb(255, 0, 0),
                StrokeThickness = 0
            };
            plotModel.Annotations.Add(g2Label);

            // Clear previous content in plotPanel
            plotPanel.Controls.Clear();

            // Create a PlotView to display the plot model
            var plotView = new OxyPlot.WindowsForms.PlotView
            {
                Model = plotModel,
                Dock = DockStyle.Fill // Dock the plotView to fill the form
            };

            // Add the PlotView to your form (assuming you have a panel named plotPanel)
            plotPanel.Controls.Add(plotView);
        }

        private void c1_Imaginary_CheckedChanged(object sender, EventArgs e)
        {
            if (c1_Imaginary.Checked)
            {
                // if checkbox selected show message
                MessageBox.Show("This checkbox is not available to change in this version", "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);

                // no able to update the check box status
                c1_Imaginary.Checked = false;
            }
        }

        private void l1_Imaginary_CheckedChanged(object sender, EventArgs e)
        {
            if (l1_Imaginary.Checked)
            {
                // if checkbox selected show message
                MessageBox.Show("This checkbox is not available to change in this version", "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);

                // no able to update the check box status
                l1_Imaginary.Checked = false;
            }
        }

        private void c2_Imaginary_CheckedChanged(object sender, EventArgs e)
        {
            if (c2_Imaginary.Checked)
            {
                // if checkbox selected show message
                MessageBox.Show("This checkbox is not available to change in this version", "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);

                // no able to update the check box status
                c2_Imaginary.Checked = false;
            }
        }

        private void l2_Imaginary_CheckedChanged(object sender, EventArgs e)
        {
            if (l2_Imaginary.Checked)
            {
                // if checkbox selected show message
                MessageBox.Show("This checkbox is not available to change in this version", "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);

                // no able to update the check box status
                l2_Imaginary.Checked = false;
            }
        }

        private void c3_Imaginary_CheckedChanged(object sender, EventArgs e)
        {
            if (c3_Imaginary.Checked)
            {
                // if checkbox selected show message
                MessageBox.Show("This checkbox is not available to change in this version", "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);

                // no able to update the check box status
                c3_Imaginary.Checked = false;
            }
        }

        private void l3_Imaginary_CheckedChanged(object sender, EventArgs e)
        {
            if (l3_Imaginary.Checked)
            {
                // if checkbox selected show message
                MessageBox.Show("This checkbox is not available to change in this version", "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);

                // no able to update the check box status
                l3_Imaginary.Checked = false;
            }
        }

        private void c1_Optimize_CheckedChanged(object sender, EventArgs e)
        {
            if (string.IsNullOrEmpty(selectedFilePath))
            {
                if (c1_Optimize.Checked)
                {
                    // if checkbox selected show message
                    MessageBox.Show("This checkbox is not available to change in this version", "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);

                    // no able to update the check box status
                    c1_Optimize.Checked = false;
                }
                    
            }
            else if (!string.IsNullOrEmpty(selectedFilePath))
            {
                if (c1_Optimize.Checked == false)
                {
                    // if checkbox selected show message
                    MessageBox.Show("This checkbox is not available to change in this version", "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);

                    // no able to update the check box status
                    c1_Optimize.Checked = true;
                }

            }


        }

        private void l1_Optimize_CheckedChanged(object sender, EventArgs e)
        {
            if (string.IsNullOrEmpty(selectedFilePath))
            {
                if (l1_Optimize.Checked)
                {
                    // if checkbox selected show message
                    MessageBox.Show("This checkbox is not available to change in this version", "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);

                    // no able to update the check box status
                    l1_Optimize.Checked = false;
                }

            }
            else if (!string.IsNullOrEmpty(selectedFilePath))
            {
                if (l1_Optimize.Checked == false)
                {
                    // if checkbox selected show message
                    MessageBox.Show("This checkbox is not available to change in this version", "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);

                    // no able to update the check box status
                    l1_Optimize.Checked = true;
                }

            }
        }

        private void c2_Optimize_CheckedChanged(object sender, EventArgs e)
        {
            if (string.IsNullOrEmpty(selectedFilePath))
            {
                if (c2_Optimize.Checked)
                {
                    // if checkbox selected show message
                    MessageBox.Show("This checkbox is not available to change in this version", "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);

                    // no able to update the check box status
                    c2_Optimize.Checked = false;
                }

            }
            else if (!string.IsNullOrEmpty(selectedFilePath))
            {
                if (c2_Optimize.Checked == false)
                {
                    // if checkbox selected show message
                    MessageBox.Show("This checkbox is not available to change in this version", "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);

                    // no able to update the check box status
                    c2_Optimize.Checked = true;
                }

            }
        }

        private void l2_Optimize_CheckedChanged(object sender, EventArgs e)
        {
            if (string.IsNullOrEmpty(selectedFilePath))
            {
                if (l2_Optimize.Checked)
                {
                    // if checkbox selected show message
                    MessageBox.Show("This checkbox is not available to change in this version", "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);

                    // no able to update the check box status
                    l2_Optimize.Checked = false;
                }

            }
            else if (!string.IsNullOrEmpty(selectedFilePath))
            {
                if (l2_Optimize.Checked == false)
                {
                    // if checkbox selected show message
                    MessageBox.Show("This checkbox is not available to change in this version", "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);

                    // no able to update the check box status
                    l2_Optimize.Checked = true;
                }

            }
        }

        private void c3_Optimize_CheckedChanged(object sender, EventArgs e)
        {
            if (string.IsNullOrEmpty(selectedFilePath))
            {
                if (c3_Optimize.Checked)
                {
                    // if checkbox selected show message
                    MessageBox.Show("This checkbox is not available to change in this version", "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);

                    // no able to update the check box status
                    c3_Optimize.Checked = false;
                }

            }
            else if (!string.IsNullOrEmpty(selectedFilePath))
            {
                if (c3_Optimize.Checked == false)
                {
                    // if checkbox selected show message
                    MessageBox.Show("This checkbox is not available to change in this version", "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);

                    // no able to update the check box status
                    c3_Optimize.Checked = true;
                }

            }
        }

        private void l3_Optimize_CheckedChanged(object sender, EventArgs e)
        {
            if (string.IsNullOrEmpty(selectedFilePath))
            {
                if (l3_Optimize.Checked)
                {
                    // if checkbox selected show message
                    MessageBox.Show("This checkbox is not available to change in this version", "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);

                    // no able to update the check box status
                    l3_Optimize.Checked = false;
                }

            }
            else if (!string.IsNullOrEmpty(selectedFilePath))
            {
                if (l3_Optimize.Checked == false)
                {
                    // if checkbox selected show message
                    MessageBox.Show("This checkbox is not available to change in this version", "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);

                    // no able to update the check box status
                    l3_Optimize.Checked = true;
                }

            }
        }

        private PlotModel CreatePlotModel()
        {
            var model = new PlotModel { Title = "Contour Heatmap" };

            int rows = 10, cols = 10;
            double[,] data = GenerateMatrix();

            var heatMap = new HeatMapSeries
            {
                X0 = 0,
                X1 = cols - 1, 
                Y0 = 0,
                Y1 = rows - 1, 
                Interpolate = true,    
                Data = data,
                ColorAxisKey = "ColorAxis"
            };

            var contourSeries = new ContourSeries
            {
                Data = data,
                ColumnCoordinates = Enumerable.Range(0, cols).Select(i => (double)i).ToArray(),
                RowCoordinates = Enumerable.Range(0, rows).Select(i => (double)i).ToArray(),
                ContourLevels = new double[] { 0.2, 0.4, 0.6, 0.8 }, 
                LabelBackground = OxyColors.White
            };

            var colorAxis = new LinearColorAxis
            {
                Position = AxisPosition.Right,
                Palette = OxyPalettes.Jet(256),
                Key = "ColorAxis"
            };

            model.Axes.Add(new LinearAxis { Position = AxisPosition.Bottom, Minimum = 0, Maximum = cols - 1 });
            model.Axes.Add(new LinearAxis { Position = AxisPosition.Left, Minimum = 0, Maximum = rows - 1 });
            model.Axes.Add(colorAxis);

            model.Series.Add(heatMap);
            model.Series.Add(contourSeries);

            return model;
        }

        private double[,] GenerateMatrix()
        {
            return new double[,] {

                //{0.05759649, 0.05759671, 0.05759658, 0.05759524, 0.05759862, 0.05759196,  0.05760199, 0.05759326, 0.05759938, 0.05759649 },
                //{ 0.05758223, 0.05758567, 0.05758377, 0.05758258, 0.05759403, 0.0575807,  0.05761298, 0.05759568, 0.05762903, 0.05764135 },
                //{ 0.05767572, 0.05767206, 0.05766544, 0.05765446, 0.05767324, 0.05758207,  0.05765799, 0.05747975, 0.05744055, 0.05730773 },
                //{ 0.05725531, 0.05732167, 0.05723584, 0.05729524, 0.05741551, 0.0572723,  0.05783385, 0.05765588, 0.05852807, 0.05886565 },
                //{ 0.05886676, 0.05880549, 0.0586603,  0.05902423, 0.05872258, 0.05774041,  0.05889533, 0.05585375, 0.05430643, 0.05219991 },
                //{ 0.05341982, 0.05418341, 0.05314872, 0.05416326, 0.0524987,  0.05245804,  0.06077991, 0.05677398, 0.07228692, 0.07594715 },
                //{ 0.06967807, 0.06966319, 0.067084,   0.07140625, 0.07138941, 0.07517331,  0.07384898, 0.03153137, 0.0119277,  0},
                //{ 0.02813599, 0.0350521,  0.02582001, 0.02389406, 0.02298216, 0.0263612,  0.00162904, 0.04155859, 0.20621108, 0.21373057 },
                //{ 0.10968703, 0.11542832, 0.10955932, 0.11153347, 0.10801819, 0.12150871,  0.06769625, 0.23320256, 1, 0.96191225 },
                //{ 0.90847521, 0.90966631, 0.90744797, 0.90924543, 0.90741041, 0.91111985,  0.90872098, 0.89670417, 0.92448758, 0.90847521 }

                {0.08465315, 0.08465276, 0.08465377, 0.08465077, 0.08465556, 0.08465066,  0.08465546, 0.08465349, 0.08465186, 0.08465315},
                {0.08465374, 0.0846534,  0.08466005, 0.08465425, 0.08467467, 0.08466138,  0.08467941, 0.08468097, 0.08467168, 0.08467496},
                {0.08465172, 0.0846439,  0.08464989, 0.08459279, 0.08463351, 0.08452134,  0.08456866, 0.08448719, 0.08450266, 0.08454897},
                {0.08465871, 0.08465595, 0.08473893, 0.08467657, 0.0850656,  0.08478976,  0.08528579, 0.08560438, 0.08511048, 0.08508704},
                { 0.08464587, 0.08460697, 0.0846498,  0.08399776, 0.08456293, 0.08221102,  0.08288696, 0.08135493, 0.08221906, 0.0835073 },
                {0.08466547, 0.08465189, 0.08497732, 0.08462891, 0.08920269, 0.08571408,  0.0957743,  0.10204302, 0.08903963, 0.08799503},
                {0.08463957, 0.08455911, 0.08474606, 0.08273391, 0.08589642, 0.05424669,  0.07054346, 0.05748548, 0.06237349, 0.08100299},
                {0.08465756, 0.0845945, 0.08522269, 0.08287948, 0.09391876, 0.06758336,  0.28315083, 0.3022502,  0.08175555, 0.0849679 }, 
                {0.08465056, 0.08452164, 0.08550045, 0.08019218, 0.10461889, 0,  0.46520289, 1,         0.02267822, 0.08522878}, 
                {0.08465315, 0.0845068,  0.0854538,  0.081216,   0.09515982, 0.05219431,  0.11691909, 0.09467228, 0.06207803, 0.08465315 }
            };
        }
    }
}
