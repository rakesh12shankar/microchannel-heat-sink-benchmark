param([double]$SlotDepthMm=3.175,[double]$SlotWidthMm=1.6,[string]$Variant='nominal',[string]$OutputRoot=(Join-Path $PSScriptRoot 'data\cad'))
$ErrorActionPreference='Stop'
$interop='C:\Program Files\SOLIDWORKS Corp\SOLIDWORKS\SolidWorks.Interop.sldworks.dll'
Add-Type -Path $interop
Add-Type -ReferencedAssemblies $interop -TypeDefinition @'
using System;
using System.IO;
using System.Text;
using System.Collections.Generic;
using SolidWorks.Interop.sldworks;
public class QuCad {
 static IModeler m;
 static IBody2 Box(double x,double y,double z,double a,double b,double c){
  IBody2 v=(IBody2)m.CreateBodyFromBox(new double[]{x+a/2,y+b/2,z,0,0,1,a,b,c});
  if(v==null)throw new Exception("Box construction failed");return v;
 }
 static IBody2 Sub(IBody2 a,IBody2 b){int e;object[] r=(object[])a.Operations2(15902,b,out e);if(e!=0||r==null||r.Length!=1)throw new Exception("Subtract failed: "+e);return (IBody2)r[0];}
 public static string Run(string dir,double depth,double width){
  Directory.CreateDirectory(dir);
  string stem="Qu_"+new DirectoryInfo(dir).Name;
  if(File.Exists(Path.Combine(dir,stem+".SLDPRT")))throw new Exception("Refusing CAD overwrite");
  ISldWorks app=(ISldWorks)Activator.CreateInstance(Type.GetTypeFromProgID("SldWorks.Application"));
  m=(IModeler)app.GetModeler();
  double L=.044764,W=.000467,baseH=.005637,chH=.000713;
  var bodies=new List<IBody2>();var names=new List<string>();
  IBody2 fluid=Box(0,.000118,baseH,L,.000231,chH);
  IBody2 copper=Sub(Box(0,0,0,L,W,baseH+chH),(IBody2)fluid.Copy());
  foreach(double center in new double[]{.010794,.022382,.033970}){
   IBody2 air=Box(center-width/2,0,0,width,W,depth);
   copper=Sub(copper,(IBody2)air.Copy());bodies.Add(air);names.Add("AirSlot_"+bodies.Count);
  }
  bodies.Insert(0,copper);names.Insert(0,"Copper");
  bodies.Add(fluid);names.Add("Water");
  bodies.Add(Box(0,0,baseH+chH,L,W,.0127));names.Add("Polycarbonate");
  IModelDoc2 doc=(IModelDoc2)app.NewDocument(@"C:\ProgramData\SOLIDWORKS\SOLIDWORKS 2019\templates\Part.prtdot",0,0,0);
  if(doc==null)throw new Exception("NewDocument failed");
  IPartDoc part=(IPartDoc)doc;var log=new StringBuilder();double total=0;
  for(int i=0;i<bodies.Count;i++){
   IFaultEntity fault=(IFaultEntity)bodies[i].Check3;if(fault!=null&&fault.Count>0)throw new Exception("Invalid CAD body");
   double vol=((double[])bodies[i].GetMassProperties(1))[3];total+=vol;
   IFeature f=(IFeature)part.CreateFeatureFromBody3(bodies[i].Copy(),false,1);if(f==null)throw new Exception("Feature failed");f.Name=names[i];
   log.AppendLine(names[i]+" volume_m3="+vol.ToString("R",System.Globalization.CultureInfo.InvariantCulture));
  }
  object[] saved=(object[])part.GetBodies2(0,false);if(saved.Length!=6)throw new Exception("Expected six bodies");
  double expected=L*W*(baseH+chH+.0127);if(Math.Abs(total-expected)/expected>1e-7)throw new Exception("Volume partition failed");
  log.AppendLine("Six valid non-overlapping solids; total volume agrees with enclosing prism within 1e-7 relative.");
  log.AppendLine("Slot depth is a reconstruction assumption; width rounded from Fig.2. SI units.");
  doc.ForceRebuild3(false);doc.ShowNamedView2("*Isometric",7);doc.ViewZoomtofit2();
  foreach(string ext in new string[]{"SLDPRT","x_t","STEP"}){int e=0,w=0;app.ActivateDoc3(doc.GetTitle(),false,0,ref e);e=0;if(!doc.Extension.SaveAs(Path.Combine(dir,stem+"."+ext),0,1,null,ref e,ref w)||e!=0)throw new Exception("Save error "+e);}
  File.WriteAllText(Path.Combine(dir,"CAD_Checks.txt"),log.ToString());return log.ToString();
 }
}
'@
[QuCad]::Run((Join-Path $OutputRoot $Variant),$SlotDepthMm/1000,$SlotWidthMm/1000)
