using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Drawing.Imaging;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using ScottPlot;
using ScottPlot.Plottable;
using ScottPlot.WinForms;
using ScottPlot.Drawing;
using System.Drawing.Drawing2D;

namespace TeamVFL_Project_Prototype
{
    public partial class contour : Form
    {
        private System.Windows.Forms.Timer updateTimer;
        private double[,] intensities;
        private int dataPoints = 20;
        private Random rand = new Random();
        private Heatmap hm;

        public contour()
        {
            InitializeComponent();
            InitializePlot();
            //SetupTimer();
        }

        private double[,] ApplyGaussianBlur(double[,] data, int kernelSize, double sigma)
        {
            double[,] blurredData = new double[data.GetLength(0), data.GetLength(1)];
            double[,] kernel = GenerateGaussianKernel(kernelSize, sigma);

            int offset = kernelSize / 2;

            for (int i = offset; i < data.GetLength(0) - offset; i++)
            {
                for (int j = offset; j < data.GetLength(1) - offset; j++)
                {
                    double sum = 0;
                    for (int k = -offset; k <= offset; k++)
                    {
                        for (int l = -offset; l <= offset; l++)
                        {
                            sum += data[i + k, j + l] * kernel[offset + k, offset + l];
                        }
                    }
                    blurredData[i, j] = sum;
                }
            }

            return blurredData;
        }

        private double[,] GenerateGaussianKernel(int size, double sigma)
        {
            double[,] kernel = new double[size, size];
            double mean = size / 2;
            double sum = 0.0;

            for (int x = 0; x < size; x++)
            {
                for (int y = 0; y < size; y++)
                {
                    kernel[x, y] = Math.Exp(-0.5 * (Math.Pow((x - mean) / sigma, 2.0) + Math.Pow((y - mean) / sigma, 2.0)))
                                   / (2 * Math.PI * sigma * sigma);
                    sum += kernel[x, y];
                }
            }

            for (int x = 0; x < size; x++)
            {
                for (int y = 0; y < size; y++)
                {
                    kernel[x, y] /= sum;
                }
            }

            return kernel;
        }


        private void InitializePlot()
        {
            // 初始化数据
            intensities = new double[dataPoints, dataPoints];
            

            Random rand = new Random();

            for (int i = 0; i < dataPoints; i++)
            {
                for (int j = 0; j < dataPoints; j++)
                {
                    double noise = PerlinNoise(i * 0.1, j * 0.1);
                    double randomFactor = rand.NextDouble() * 0.5;

                    intensities[i, j] = noise * 0.5 + randomFactor;
                }
            }

            intensities = ApplyGaussianBlur(intensities, 5, 1.0);

            // 配置热图
            //var hm = formsPlot2.Plot.AddHeatmap(intensities);
            hm = formsPlot2.Plot.AddHeatmap(intensities, colormap: CreateCustomColormap());
            GenerateColorbar();


            // 设置颜色映射
            //hm.Update(intensities, ScottPlot.Drawing.Colormap.Turbo);

            formsPlot2.Plot.Legend();

            // 配置坐标轴
            formsPlot2.Plot.XLabel("X Axis");
            formsPlot2.Plot.YLabel("Y Axis");
            formsPlot2.Plot.Title("Dynamic Contour Heatmap");

            // 刷新显示
            formsPlot2.Refresh();
        }

        private double PerlinNoise(double x, double y)
        {
            return Math.Sin(x * 3.14) * Math.Cos(y * 3.14);
        }


        private Colormap CreateCustomColormap()
        {
            // 关键颜色点
            Color[] colors = new Color[]
            {
                Color.Red,      // 红色
                Color.Orange,   // 橙色
                Color.Yellow,   // 黄色
                Color.Green,    // 绿色
                Color.Blue // 浅蓝
            };

            // 生成插值渐变
            int steps = 1024; // 颜色渐变步长
            Color[] smoothColors = GenerateSmoothGradient(colors, steps);

            // 创建 ScottPlot Colormap
            return new Colormap(smoothColors);
        }

        private Color[] GenerateSmoothGradient(Color[] keyColors, int steps)
        {
            List<Color> smoothColors = new List<Color>();

            for (int i = 0; i < keyColors.Length - 1; i++)
            {
                Color startColor = keyColors[i];
                Color endColor = keyColors[i + 1];

                for (int j = 0; j < steps / (keyColors.Length - 1); j++)
                {
                    float t = j / (float)(steps / (keyColors.Length - 1) - 1); // 归一化 [0,1]
                    Color blendedColor = Color.FromArgb(
                        (int)(startColor.R + (endColor.R - startColor.R) * t),
                        (int)(startColor.G + (endColor.G - startColor.G) * t),
                        (int)(startColor.B + (endColor.B - startColor.B) * t)
                    );
                    smoothColors.Add(blendedColor);
                }
            }

            return smoothColors.ToArray();
        }



        private void GenerateColorbar()
        {
            int width = 50;  
            int height = 300; 
            Bitmap bitmap = new Bitmap(width, height);

            using (Graphics g = Graphics.FromImage(bitmap))
            {
                for (int y = 0; y < height; y++)
                {
                    double value = (double)y / (height - 1);

                    Color color = GetSmoothColor(value);

                    using (Pen pen = new Pen(color))
                    {
                        g.DrawLine(pen, 0, height - y, width, height - y);
                    }
                }
            }

            pictureBox1.Image = bitmap;
        }

        private Color GetSmoothColor(double value)
        {
            Color[] colors = new Color[]
            {
                Color.Red,       
                Color.Orange,    
                Color.Yellow,    
                Color.Green,     
                Color.Blue
            };

            double[] positions = new double[]
            {
                0.0,  
                0.25,  
                0.5,  
                0.75,  
                1.0   
            };

            for (int i = 0; i < positions.Length - 1; i++)
            {
                if (value >= positions[i] && value <= positions[i + 1])
                {
                    double t = (value - positions[i]) / (positions[i + 1] - positions[i]);
                    return InterpolateColor(colors[i], colors[i + 1], t);
                }
            }

            return colors[colors.Length - 1]; 
        }
        private Color InterpolateColor(Color color1, Color color2, double t)
        {
            int r = (int)(color1.R + t * (color2.R - color1.R));
            int g = (int)(color1.G + t * (color2.G - color1.G));
            int b = (int)(color1.B + t * (color2.B - color1.B));
            return Color.FromArgb(r, g, b);
        }



        //private void SetupTimer()
        //{
        //    updateTimer = new System.Windows.Forms.Timer();
        //    updateTimer.Interval = 100; // 更新间隔(毫秒)
        //    updateTimer.Tick += UpdateTimer_Tick;
        //    updateTimer.Start();
        //}

        //private void UpdateTimer_Tick(object sender, EventArgs e)
        //{
        //    // 更新数据
        //    for (int i = 0; i < dataPoints; i++)
        //    {
        //        for (int j = 0; j < dataPoints; j++)
        //        {
        //            double time = DateTime.Now.Millisecond / 1000.0;
        //            intensities[i, j] = Math.Sin(i * 0.2 + time) * Math.Cos(j * 0.2 + time)
        //                              + rand.NextDouble() * 0.1;
        //        }
        //    }

        //    // 更新热图
        //    var hm = formsPlot2.Plot.AddHeatmap(intensities);


        //    // 刷新显示
        //    formsPlot2.Refresh();
        //}

    }
}