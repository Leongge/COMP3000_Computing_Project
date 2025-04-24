using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Newtonsoft.Json;
using OxyPlot.Annotations;
using OxyPlot.Axes;
using OxyPlot;
using Python.Runtime;
using ScottPlot;
using OxyPlot.Series;
using System.IO;
using System.Reflection;
using System.Diagnostics;

namespace TeamVFL_Project_Prototype
{
    public partial class Contour : Form
    {
        private PlotModel plotModel;
        private LineSeries s11Series;
        private LineSeries s12Series;
        private LineSeries s21Series;
        private LineSeries s22Series;
        private string selectedFilePath;
        public dynamic PyLauncher;
        private StringBuilder matrixBuffer = new StringBuilder();
        private int matrixCount = 0;
        private bool isCollectingMatrix = false;
        private const int MATRIX_SIZE = 10;
        private string cleanedJson;
        private bool Optimized;
        private List<double[,]> currentMatrices = new List<double[,]>();
        private List<OxyPlot.WindowsForms.PlotView> plotViews;

        public Contour()
        {
            InitializeComponent();
            InitializePlotViews();
            string basePath = Path.Combine(Directory.GetCurrentDirectory());
            string hflibPath = Path.Combine(Directory.GetCurrentDirectory(), @"hflib");
            string python39 = Path.Combine(Directory.GetCurrentDirectory(), @"common\python39\python39.dll");
            //string python311 = Path.Combine(Directory.GetCurrentDirectory(), @"common\python311\python311.dll");
            string modulePath = Path.Combine(Directory.GetCurrentDirectory(), @"common\pythonlib");
            string modulePath2 = Path.Combine(Directory.GetCurrentDirectory(), @"common\pythonlib2");
            string envPath = Path.Combine(Directory.GetCurrentDirectory(), @"common\python39");
            string envPath2 = Path.Combine(Directory.GetCurrentDirectory(), @"common\python311");
            string oriPath = Environment.GetEnvironmentVariable("PATH")?.TrimEnd(Path.PathSeparator);
            oriPath = string.IsNullOrEmpty(oriPath) ? envPath : oriPath + Path.PathSeparator + envPath;

            // Set Environment Variables
            Environment.SetEnvironmentVariable("PATH", oriPath, EnvironmentVariableTarget.Process);
            Environment.SetEnvironmentVariable("PYTHONNET_PYDLL", python39);
            Environment.SetEnvironmentVariable("PYTHONPATH", $"{modulePath}{Path.PathSeparator}{basePath}{Path.PathSeparator}{hflibPath}", EnvironmentVariableTarget.Process);

            // Set Environment Variables for python 311
            //Environment.SetEnvironmentVariable("PATH", oriPath, EnvironmentVariableTarget.Process);
            //Environment.SetEnvironmentVariable("PYTHONNET_PYDLL", python311);
            //Environment.SetEnvironmentVariable("PYTHONPATH", $"{modulePath2}{Path.PathSeparator}{basePath}{Path.PathSeparator}{hflibPath}", EnvironmentVariableTarget.Process);


            // Initialize Python Engine
            PythonEngine.PythonPath = PythonEngine.PythonPath + Path.PathSeparator + Environment.GetEnvironmentVariable("PYTHONPATH", EnvironmentVariableTarget.Process);
            PythonEngine.Initialize();

            // Initialize the launcher, first import launch.pyd, then initialize its class constructor
            using (Py.GIL())
            {
                dynamic launcher = Py.Import("launch");
                PyLauncher = launcher.HFLaunch();
            }

            // Set initial checkbox states
            checkboxS11.Checked = true;
            checkboxS12.Checked = true;

            checkboxS11.CheckedChanged += CheckboxS11_CheckedChanged;
            checkboxS12.CheckedChanged += CheckboxS12_CheckedChanged;
            checkboxS21.CheckedChanged += CheckboxS21_CheckedChanged;
            checkboxS22.CheckedChanged += CheckboxS22_CheckedChanged;

            selectedFilePath = @"C:\Users\leong\OneDrive\Documents\Peninsula Collegue\Study\Year 3 Sem 2\FYP\FYP_BSSE2309678\vflproject\backend\aiora-metric-vC2\Trainer\EDSHF_designs\2p-EPU2D\2p-EPU2D.fpx";
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
            if (!string.IsNullOrEmpty(selectedFilePath) && Optimized == false)
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

        private void ShowGraph_Click(object sender, EventArgs e)
        {
            ProcessFileAndGenerateChart();
        }

        private void ProcessFileAndGenerateChart()
        {
            PyObject output = null;

            using (Py.GIL())
            {
                output = PyLauncher.load_design(selectedFilePath);
            }
            //outputTextBox.Text = output.ToString();

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
                MajorGridlineStyle = OxyPlot.LineStyle.Solid,
                MinorGridlineStyle = OxyPlot.LineStyle.Dot,
                Key = "FrequencyAxis"
            });
            plotModel.Axes.Add(new OxyPlot.Axes.LinearAxis
            {
                Position = AxisPosition.Left,
                MajorGridlineStyle = OxyPlot.LineStyle.Solid,
                MinorGridlineStyle = OxyPlot.LineStyle.Dot,
                Title = "dB"
            });

            var g0Line = new LineAnnotation
            {
                Type = LineAnnotationType.Horizontal,
                Y = Convert.ToDouble(-18),
                Color = OxyColor.FromRgb(0, 255, 0),
                LineStyle = OxyPlot.LineStyle.DashDot
            };
            g0Line.MinimumX = Convert.ToDouble(1.429);
            g0Line.MaximumX = Convert.ToDouble(1.512);
            plotModel.Annotations.Add(g0Line);


            var g0Label = new TextAnnotation
            {
                Text = "g0",
                TextPosition = new DataPoint((g0Line.MinimumX + g0Line.MaximumX) / 2, g0Line.Y),
                TextVerticalAlignment = OxyPlot.VerticalAlignment.Bottom,
                TextHorizontalAlignment = OxyPlot.HorizontalAlignment.Center,
                TextColor = OxyColor.FromRgb(0, 255, 0),
                StrokeThickness = 0
            };
            plotModel.Annotations.Add(g0Label);


            var g1Line = new LineAnnotation
            {
                Type = LineAnnotationType.Horizontal,
                Y = Convert.ToDouble(-25),
                Color = OxyColor.FromRgb(255, 0, 0),
                LineStyle = OxyPlot.LineStyle.DashDot
            };
            g1Line.MinimumX = Convert.ToDouble(1.3);
            g1Line.MaximumX = Convert.ToDouble(1.42);
            plotModel.Annotations.Add(g1Line);
            var g1Label = new TextAnnotation
            {
                Text = "g1",
                TextPosition = new DataPoint((g1Line.MinimumX + g1Line.MaximumX) / 2, g1Line.Y),
                TextVerticalAlignment = OxyPlot.VerticalAlignment.Bottom,
                TextHorizontalAlignment = OxyPlot.HorizontalAlignment.Center,
                TextColor = OxyColor.FromRgb(255, 0, 0),
                StrokeThickness = 0
            };
            plotModel.Annotations.Add(g1Label);


            var g2Line = new LineAnnotation
            {
                Type = LineAnnotationType.Horizontal,
                Y = Convert.ToDouble(-25),
                Color = OxyColor.FromRgb(255, 0, 0),
                LineStyle = OxyPlot.LineStyle.DashDot
            };
            g2Line.MinimumX = Convert.ToDouble(1.525);
            g2Line.MaximumX = Convert.ToDouble(1.65);
            plotModel.Annotations.Add(g2Line);

            var g2Label = new TextAnnotation
            {
                Text = "g2",
                TextPosition = new DataPoint((g2Line.MinimumX + g2Line.MaximumX) / 2, g2Line.Y),
                TextVerticalAlignment = OxyPlot.VerticalAlignment.Bottom,
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

        private void InitializePlotViews()
        {
            // 假设你已经在表单设计器中创建了9个plotView控件
            plotViews = new List<OxyPlot.WindowsForms.PlotView>
            {
                contour1, contour2, contour3,
                contour4, contour5, contour6,
                contour7, contour8, contour9
            };

            // 初始化每个PlotView的模型
            foreach (var view in plotViews)
            {
                view.Model = new PlotModel { Title = "Waiting for data..." };
            }

            
        }

        private void btn_optimize_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrEmpty(selectedFilePath))
            {
                MessageBox.Show("No Path Selected");
                return;
            }

            // 保存当前环境变量
            string originalPath = Environment.GetEnvironmentVariable("PATH");
            string originalPythonDll = Environment.GetEnvironmentVariable("PYTHONNET_PYDLL");
            string originalPythonPath = Environment.GetEnvironmentVariable("PYTHONPATH");

            try
            {
                // 设置Python 3.11环境
                string envPath2 = Path.Combine(Directory.GetCurrentDirectory(), @"common\python311");
                string python311 = Path.Combine(Directory.GetCurrentDirectory(), @"common\python311\python311.dll");
                string modulePath2 = Path.Combine(Directory.GetCurrentDirectory(), @"common\pythonlib2");
                string basePath = Directory.GetCurrentDirectory();
                string hflibPath = Path.Combine(Directory.GetCurrentDirectory(), @"hflib");

                string oriPath = originalPath?.TrimEnd(Path.PathSeparator);
                oriPath = string.IsNullOrEmpty(oriPath) ? envPath2 : oriPath + Path.PathSeparator + envPath2;

                Environment.SetEnvironmentVariable("PATH", oriPath, EnvironmentVariableTarget.Process);
                Environment.SetEnvironmentVariable("PYTHONNET_PYDLL", python311);
                Environment.SetEnvironmentVariable("PYTHONPATH", $"{modulePath2}{Path.PathSeparator}{basePath}{Path.PathSeparator}{hflibPath}", EnvironmentVariableTarget.Process);

                // 获取Python脚本路径
                string currentDir = Directory.GetCurrentDirectory();
                string projectDir = Directory.GetParent(currentDir)?.Parent?.Parent?.Parent?.FullName;
                if (projectDir == null)
                {
                    MessageBox.Show("Cannot determine project directory");
                    return;
                }

                string pythonScriptPath = Path.Combine(projectDir, @"backend\aiora-metric-vC2\Trainer\run_model_vC.py");
                if (!File.Exists(pythonScriptPath))
                {
                    MessageBox.Show($"Python script not found at: {pythonScriptPath}");
                    return;
                }

                // 运行Python脚本
                string pythonExePath = Path.Combine(Directory.GetCurrentDirectory(), @"common\python311\python.exe");
                if (!File.Exists(pythonExePath))
                {
                    MessageBox.Show($"Python executable not found at: {pythonExePath}");
                    return;
                }

                Optimize_output.Clear();

                ProcessStartInfo startInfo = new ProcessStartInfo
                {
                    FileName = pythonExePath,
                    Arguments = $"\"{pythonScriptPath}\"",  // 确保路径有引号
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    CreateNoWindow = true
                };

                // 确保Python输出不使用缓冲区
                startInfo.EnvironmentVariables["PYTHONUNBUFFERED"] = "1";

                Process process = new Process
                {
                    StartInfo = startInfo,
                    EnableRaisingEvents = true
                };

                // 设置异步事件处理器来实时读取输出
                process.OutputDataReceived += (s, args) =>
                {
                    if (args.Data != null)
                    {
                        UpdateOutputTextBox(args.Data);
                    }
                };

                process.ErrorDataReceived += (s, args) =>
                {
                    if (args.Data != null)
                    {
                        UpdateOutputTextBox($"ERROR: {args.Data}");
                    }
                };

                process.Start();

                // 开始异步读取
                process.BeginOutputReadLine();
                process.BeginErrorReadLine();

                // 在后台线程等待进程完成
                Task.Run(() =>
                {
                    process.WaitForExit();
                    UpdateOutputTextBox($"Process completed with exit code: {process.ExitCode}");

                    // 恢复原始环境变量
                    Environment.SetEnvironmentVariable("PATH", originalPath);
                    Environment.SetEnvironmentVariable("PYTHONNET_PYDLL", originalPythonDll);
                    Environment.SetEnvironmentVariable("PYTHONPATH", originalPythonPath);

                    this.Invoke(new Action(() =>
                    {
                        UpdateGraph();
                    }));
                });
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error: {ex.Message}\n\nStack Trace: {ex.StackTrace}");

                // 确保在异常情况下也恢复环境变量
                Environment.SetEnvironmentVariable("PATH", originalPath);
                Environment.SetEnvironmentVariable("PYTHONNET_PYDLL", originalPythonDll);
                Environment.SetEnvironmentVariable("PYTHONPATH", originalPythonPath);
            }
        }

        // 辅助方法：线程安全地更新输出文本框
        private void UpdateOutputTextBox(string text)
        {
            if (Optimize_output.InvokeRequired)
            {
                Optimize_output.Invoke(new Action(() =>
                {
                    ProcessOutputLine(text);
                }));
            }
            else
            {
                ProcessOutputLine(text);
            }
        }

        private void ProcessOutputLine(string line)
        {
            // 添加到输出文本框
            Optimize_output.AppendText(line + Environment.NewLine);

            // 自动滚动到底部
            Optimize_output.SelectionStart = Optimize_output.Text.Length;
            Optimize_output.ScrollToCaret();

            // 检查是否是新的观测结果开始
            if (line.Contains("Best Cost:") && line.Contains("Actions:"))
            {
                // 如果有收集的矩阵，先处理它们
                if (currentMatrices.Count > 0)
                {
                    UpdateContourPlots(currentMatrices);
                }

                // 重置矩阵收集状态
                currentMatrices.Clear();
                isCollectingMatrix = false;
                matrixBuffer.Clear();

                // 显示新的观测信息
                UpdateObservationInfo(line);
            }

            // 检查是否是矩阵数据的开始
            if (line.Trim().StartsWith("[") && line.Contains(" ") && !isCollectingMatrix)
            {
                isCollectingMatrix = true;
                matrixBuffer.Clear();
                matrixBuffer.Append(line);
            }
            // 如果正在收集矩阵数据，继续追加
            else if (isCollectingMatrix)
            {
                matrixBuffer.Append(line);

                // 检查是否到达矩阵结束
                if (line.Trim().EndsWith("]"))
                {
                    // 处理完整的矩阵
                    double[,] matrix = ParseMatrix(matrixBuffer.ToString());
                    if (matrix != null)
                    {
                        currentMatrices.Add(matrix);

                        // 如果已经收集到了足够的矩阵，更新轮廓图
                        if (currentMatrices.Count == 9)
                        {
                            UpdateContourPlots(currentMatrices);
                            currentMatrices.Clear();
                        }
                    }

                    // 重置矩阵收集状态
                    isCollectingMatrix = false;
                    matrixBuffer.Clear();
                }
            }
        }

        private double[,] ParseMatrix(string matrixText)
        {
            try
            {
                // 移除所有括号和多余空格
                string cleanText = matrixText.Replace("[", "").Replace("]", "").Trim();

                // 按空格分割所有数字
                string[] values = cleanText.Split(new[] { ' ', '\n', '\r', '\t' }, StringSplitOptions.RemoveEmptyEntries);

                // 创建10x10矩阵
                double[,] matrix = new double[MATRIX_SIZE, MATRIX_SIZE];

                // 填充矩阵
                for (int i = 0; i < values.Length && i < MATRIX_SIZE * MATRIX_SIZE; i++)
                {
                    int row = i / MATRIX_SIZE;
                    int col = i % MATRIX_SIZE;

                    if (double.TryParse(values[i], out double val))
                    {
                        matrix[row, col] = val;
                    }
                }

                return matrix;
            }
            catch (Exception ex)
            {
                Debug.WriteLine($"Error parsing matrix: {ex.Message}");
                return null;
            }
        }

        private void UpdateContourPlots(List<double[,]> matrices)
        {
            // 确保在UI线程上执行
            if (this.InvokeRequired)
            {
                this.Invoke(new Action(() => UpdateContourPlots(matrices)));
                return;
            }

            // 更新每个PlotView
            for (int i = 0; i < Math.Min(matrices.Count, plotViews.Count); i++)
            {
                plotViews[i].Model = CreatePlotModel(matrices[i], $"Matrix {i + 1}");
                plotViews[i].InvalidatePlot(true);
            }
        }

        private PlotModel CreatePlotModel(double[,] data, string title)
        {
            var model = new PlotModel { Title = title };
            int rows = data.GetLength(0);
            int cols = data.GetLength(1);

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

        private void UpdateObservationInfo(string info)
        {
            // 提取关键信息并显示
            string[] parts = info.Split('|');
            if (parts.Length >= 3)
            {
                string design = parts[0].Trim();
                string iteration = parts[1].Trim();
                string costAndActions = parts[2].Trim();

                //// 在某个标签控件上显示这些信息
                //if (lblObservationInfo != null && lblObservationInfo.InvokeRequired)
                //{
                //    lblObservationInfo.Invoke(new Action(() =>
                //    {
                //        lblObservationInfo.Text = $"{design} | Iteration: {iteration} | {costAndActions}";
                //    }));
                //}
                //else if (lblObservationInfo != null)
                //{
                //    lblObservationInfo.Text = $"{design} | Iteration: {iteration} | {costAndActions}";
                //}
            }
        }

        private void UpdateGraph()
        {
            string currentFilePath = Assembly.GetExecutingAssembly().Location;
            Console.WriteLine("Current File Path: " + currentFilePath);

            DirectoryInfo currentDirectory = new DirectoryInfo(Path.GetDirectoryName(currentFilePath));
            DirectoryInfo projectDirectory = currentDirectory.Parent.Parent.Parent.Parent;
            Console.WriteLine("Project Directory Path: " + projectDirectory.FullName);

            string relativePath = @"pythonAPI\vfl_marl_version1.0\update_graph2.py";
            string updateGraphScriptPath = Path.Combine(projectDirectory.FullName, relativePath);

            if (File.Exists(updateGraphScriptPath))
            {
                // Split the bestParameters string into individual values
                //string[] parametersArray = bestParameters.Replace("[", "").Replace("]", "").Split(',');

                //// Trim and convert each parameter to string
                //for (int i = 0; i < parametersArray.Length; i++)
                //{
                //    parametersArray[i] = parametersArray[i].Trim();
                //}
                // Construct the arguments string with individual parameters
                string pythonPath = Path.Combine(projectDirectory.FullName, @"TeamVFL_Project_Prototype\bin\x64\Release\common\python39\python.exe");
                string scriptPath = $"\"{updateGraphScriptPath}\"";
                //string arguments = $"{parametersArray[0]} {parametersArray[1]} {parametersArray[2]} {parametersArray[3]} {parametersArray[4]} {parametersArray[5]}";
                PyObject output = ExecutePythonScriptObject(scriptPath);
                Console.WriteLine(output.ToString());
                cleanedJson = output.ToString().Replace("None", "null").Replace("True", "true"); ;
                Console.WriteLine(cleanedJson);
                // Accessing component values
                ProcessJsonResponse(cleanedJson);
                Optimized = true;

            }
            else
            {
                Console.WriteLine("update_graph2.py not found!");
            }
        }

        private PyObject ExecutePythonScriptObject(string scriptName)
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
                Arguments = $"{scriptName} ",
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
                MajorGridlineStyle = OxyPlot.LineStyle.Solid,
                MinorGridlineStyle = OxyPlot.LineStyle.Dot,
                Key = "FrequencyAxis"
            });
            plotModel.Axes.Add(new OxyPlot.Axes.LinearAxis
            {
                Position = AxisPosition.Left,
                MajorGridlineStyle = OxyPlot.LineStyle.Solid,
                MinorGridlineStyle = OxyPlot.LineStyle.Dot,
                Title = "dB"
            });

            var g0Line = new LineAnnotation
            {
                Type = LineAnnotationType.Horizontal,
                Y = Convert.ToDouble(-18.0),
                Color = OxyColor.FromRgb(0, 255, 0),
                LineStyle = OxyPlot.LineStyle.DashDot
            };
            g0Line.MinimumX = Convert.ToDouble(1.429);
            g0Line.MaximumX = Convert.ToDouble(1.512);
            plotModel.Annotations.Add(g0Line);


            var g0Label = new TextAnnotation
            {
                Text = "g0",
                TextPosition = new DataPoint((g0Line.MinimumX + g0Line.MaximumX) / 2, g0Line.Y),
                TextVerticalAlignment = OxyPlot.VerticalAlignment.Bottom,
                TextHorizontalAlignment = OxyPlot.HorizontalAlignment.Center,
                TextColor = OxyColor.FromRgb(0, 255, 0),
                StrokeThickness = 0
            };
            plotModel.Annotations.Add(g0Label);


            var g1Line = new LineAnnotation
            {
                Type = LineAnnotationType.Horizontal,
                Y = Convert.ToDouble(-25),
                Color = OxyColor.FromRgb(255, 0, 0),
                LineStyle = OxyPlot.LineStyle.DashDot
            };
            g1Line.MinimumX = Convert.ToDouble(1.3);
            g1Line.MaximumX = Convert.ToDouble(1.42);
            plotModel.Annotations.Add(g1Line);
            var g1Label = new TextAnnotation
            {
                Text = "g1",
                TextPosition = new DataPoint((g1Line.MinimumX + g1Line.MaximumX) / 2, g1Line.Y),
                TextVerticalAlignment = OxyPlot.VerticalAlignment.Bottom,
                TextHorizontalAlignment = OxyPlot.HorizontalAlignment.Center,
                TextColor = OxyColor.FromRgb(255, 0, 0),
                StrokeThickness = 0
            };
            plotModel.Annotations.Add(g1Label);


            var g2Line = new LineAnnotation
            {
                Type = LineAnnotationType.Horizontal,
                Y = Convert.ToDouble(-25),
                Color = OxyColor.FromRgb(255, 0, 0),
                LineStyle = OxyPlot.LineStyle.DashDot
            };
            g2Line.MinimumX = Convert.ToDouble(1.525);
            g2Line.MaximumX = Convert.ToDouble(1.65);
            plotModel.Annotations.Add(g2Line);

            var g2Label = new TextAnnotation
            {
                Text = "g2",
                TextPosition = new DataPoint((g2Line.MinimumX + g2Line.MaximumX) / 2, g2Line.Y),
                TextVerticalAlignment = OxyPlot.VerticalAlignment.Bottom,
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

    }
}
