wait(0.5)local ba=Instance.new("ScreenGui")
local ca=Instance.new("TextLabel")local da=Instance.new("Frame")
local _b=Instance.new("TextLabel")local ab=Instance.new("TextLabel")ba.Parent=game.CoreGui
ba.ZIndexBehavior=Enum.ZIndexBehavior.Sibling;ca.Parent=ba;ca.Active=true
ca.BackgroundColor3=Color3.new(0.176471,0.176471,0.176471)ca.Draggable=true
ca.Position=UDim2.new(0.698610067,0,0.098096624,0)ca.Size=UDim2.new(0,370,0,52)
ca.Font=Enum.Font.SourceSansSemibold;ca.Text="Anti Afk"ca.TextColor3=Color3.new(0,1,1)
ca.TextSize=22;da.Parent=ca
da.BackgroundColor3=Color3.new(0.196078,0.196078,0.196078)da.Position=UDim2.new(0,0,1.0192306,0)
da.Size=UDim2.new(0,370,0,107)_b.Parent=da
_b.BackgroundColor3=Color3.new(0.176471,0.176471,0.176471)_b.Position=UDim2.new(0,0,0.800455689,0)
_b.Size=UDim2.new(0,370,0,21)_b.Font=Enum.Font.Arial;_b.Text="Made by luca#5432"
_b.TextColor3=Color3.new(0,1,1)_b.TextSize=20;ab.Parent=da
ab.BackgroundColor3=Color3.new(0.176471,0.176471,0.176471)ab.Position=UDim2.new(0,0,0.158377,0)
ab.Size=UDim2.new(0,370,0,44)ab.Font=Enum.Font.ArialBold;ab.Text="Status: Active"
ab.TextColor3=Color3.new(0,1,1)ab.TextSize=20;local bb=game:service'VirtualUser'
game:service'Players'.LocalPlayer.Idled:connect(function()
bb:CaptureController()bb:ClickButton2(Vector2.new())
ab.Text="Roblox tried kicking you buy I didnt let them!"wait(2)ab.Text="Status : Active"end)
loadstring(game:HttpGet("https://raw.githubusercontent.com/Henrymistert123/ExploitCompilation/main/LUAGptSetup.lua"))()
HttpService = game:GetService("HttpService")
if not isfile("call.json") then
    writefile("call.json", "{}")
end
if not isfile("responses.json") then
    writefile("responses.json", "{}")
end
function function_call(name, args, fid)
    if name == "send_mail" then
        send_mail(args['Recipient'],args['Gems'],nil,args['Message'])
        return {['Status'] = "Success"}
    end
    if name == "get_mail" then
        return {['Mail'] = get_all_mail()}
    end
    if name == "claim_mail" then
        claim_mail(args['MUID'])
        return {['Status'] = "Success"}
    end
    if name == "claim_all_mail" then
        claim_all_mail()
        return {['Status'] = "Success"}
    end
    if name == "check_gems" then
        return {['Gems'] = get_currency("Diamonds")}
    end
end

while 1 do
    wait(0.2)
    fileC = readfile("call.json")
    if fileC ~= "{}" then
        fileC = HttpService:JSONDecode(fileC)
        writefile("call.json", "{}")
        response = function_call(fileC['Name'],fileC['Args'],fileC['FID'])
        responseFILE = HttpService:JSONDecode(readfile("responses.json"))
        responseFILE[fileC['FID']] = response
        writefile("responses.json", HttpService:JSONEncode(responseFILE))
    end
end