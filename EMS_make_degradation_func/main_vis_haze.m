clc;
clear all;

% Set file paths for input and output image directories
file_path = '';
out_path = '';

% Get a list of all JPG images in the specified directory
img_path_list = dir(fullfile(file_path, '*.jpg'));
img_num = length(img_path_list); % Total number of images
I = cell(1, img_num); % Preallocate cell array for images

% Process each image if there are any available
if img_num > 0
    for j = 1:img_num
        image_name = img_path_list(j).name; % Image name
        image = imread(fullfile(file_path, image_name)); % Read the image
        
        % Apply fog effect to the image
        Iw = add_fog(image);
        
        % Display processing status
        fprintf('%d %d %s\n', j, img_num, fullfile(file_path, image_name));
        
        % Save the processed image
        imwrite(Iw, fullfile(out_path, image_name));
    end
end

% Function to add fog effect to an image
function [Iw] = add_fog(I)
    I1 = double(I) / 255; % Normalize the image
    [row, col, z] = size(I1); % Get image dimensions
    Iw = I1; % Initialize output image

    % Fog parameters
    m = 100;
    n = 300;
    landline = 0; % Landline position
    A = 0.8; % Fog strength parameter

    % Loop through different values of beta for fog effect
    for beta = 0.04:0.04:0.12
        % Process each pixel in the image
        for i = 1:3 % Loop over RGB channels
            for j = landline + 1:row
                for l = 1:col
                    d(j, l) = 1 / ((j - landline) ^ 0.05 + 0.0001); % Depth calculation
                    d2(j, l) = d(j, l) * 8; % Adjusted depth for calculation

                    if j < landline
                        d(j, l) = -0.04 * landline + 18; % Default value above landline
                        td(j, l) = exp(-beta * d(j, l)); % Transmission degree
                        Iw(j, l, i) = I1(landline, l, i) * td(landline, l) + A * (1 - td(j, l));
                    else
                        d(j, l) = -0.04 * sqrt((j - m)^2 + (l - n)^2) + 17; % Fog depth based on distance
                        td(j, l) = exp(-beta * d(j, l)); % Transmission degree
                        Iw(j, l, i) = I1(j, l, i) * td(j, l) + A * (1 - td(j, l)); % Apply fog effect
                    end
                end
            end
        end
        
        % Set landline rows to the fogged value
        for k = 1:landline
            for kj = 1:col
                Iw(k, kj, :) = Iw(landline + 1, 100, :); % Copy fogged value
            end
        end
    end
end



