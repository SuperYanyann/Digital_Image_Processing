%% 3D_reconstruction
% auther : Yan Wang
% date : 2018/10/19
%% clear data and get "cameraParams"
% should get "cameraParams" by "camera calibration" before
clc

%% get the path of img which need to be reconstructed
binary_dir = 'F:\My_CS\Êý×ÖÍ¼Ïñ´¦Àí\project4\photo\test8\binary';
num_photo = 8;

%% load imgs and read the info of them
img_set = imageSet(binary_dir);
temp_img = read(img_set, 1);
[row, col] = size(temp_img);

%% orthodontic distortion
binary_images = cell(1, num_photo);
for i = 1:num_photo
    % read the binary img
    src_filename = img_set.ImageLocation{i};
    [src_path,src_name,src_ext] = fileparts(src_filename);
    temp_filename = strcat(src_name,src_ext);
    binary_filename = fullfile(binary_dir, temp_filename);
    binary_Img = imread(binary_filename);
    %Attention : use "undistortImage" to orthodontic distortion
    undistortedImage = undistortImage(binary_Img, cameraParams);
    binary_images{i} = undistortedImage;
end

%% build a cuboid surround the cuboid
[x,y,z] = meshgrid(60:0.5:120, 200:0.5:320, -90:0.5:0);
num_points = length(x(:));
cuboid = [x(:),y(:),z(:), ones(num_points, 1)];

%% get the point in the cuboid
loop_point = ones(num_points, 1);
K = cameraParams.IntrinsicMatrix;
figure;
for j = 1:num_photo
    % transform the world coordinate system to pixel coordinate system
    fprintf('begin check points in photo: %d\n', j);
    R = cameraParams.RotationMatrices(:,:,j);
    T = cameraParams.TranslationVectors(j,:);
    temp_pixel = cuboid * [R;T] * K;
    s = temp_pixel(:,3);
    system_pixel = [temp_pixel(:,1)./s, temp_pixel(:,2)./s];
    
    % loop the point between all pictures one by one
    % if the point is not in the picture,the point is eliminated.
    pixel_row = round(system_pixel(:,2));
    pixel_col = round(system_pixel(:,1));
    % point of existence in the photo
    temp_point = binary_images{j}(pixel_row + (pixel_col-1)*row)>0;
    % point of existence in all photo
    loop_point = loop_point & temp_point;

    % put points into the binary_img 
    % to check whether the corresponding relationship between points is correct.
    subplot(3,3,j);
    imshow(binary_images{j});
    hold on;
    indices = find(loop_point);
    system_pixel_remain = system_pixel(indices(1:2:end),:);
    plot(system_pixel_remain(:,1),system_pixel_remain(:,2),'r.');
    hold off;
end

%% get the point of existence
cuboid = cuboid(loop_point,:);

%% show the points
figure; 
pcshow([cuboid(:,1), cuboid(:,2), -cuboid(:,3)]);
fprintf('finish !!!\n');