function checksum = checksum(s)

%calculate checksum for the structure s

checksum = int32(-1);

if ~isstruct(s)
    fprintf('Input must be structure\n');
    return
end

% structure fields
f = fieldnames(s);

for fi = 1:length(f)
    switch class(s.(f{fi}))
        case {'struct' 'cell'}
            %skip sub-structure or cell array
        case 'char'
            checksum = checksum - sum(uint8(s.(f{fi})));
        otherwise
            %first input to typecast should be vector
            checksum = checksum - sum(typecast(s.(f{fi})(:), 'uint8'));
    end
end
