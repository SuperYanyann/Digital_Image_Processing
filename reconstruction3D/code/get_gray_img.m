%% get the gray photo of all photos
% auther : Yan Wang
% date : 2018/10/19
clear
clc
% get the path of img and output
img_Path = 'F:\My_CS\数字图像处理\project4\photo\test8\real\';
output_Path = 'F:\My_CS\数字图像处理\project4\photo\test8\binary\';
imgDir = dir([img_Path '*.jpg']); 
% operate
for i = 1:length(imgDir)  
    ori_img = imread([img_Path imgDir(i).name]);
    % get gray img
    gray_img = rgb2gray(ori_img);
    % get binary img
    thresh = graythresh(gray_img);  
    binary_img = im2bw(gray_img,thresh);
    binary_img = ~binary_img;
    % write img into the file
    output_name =imgDir(i).name;
    save_path=[output_Path,output_name];    
    imwrite(binary_img,save_path);
    
    fprintf('finish the %d photo\n',i)
end
