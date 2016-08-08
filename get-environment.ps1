<#
    .DESCRIPTION
    Gets the environment variables needed to run the Killrvideo docker-compose commands and outputs
    them to stdout.
#>
[CmdletBinding()]
Param ()

# Figure out if we're Docker for Windows or Docker Toolbox setup
Write-Host 'Determining docker installation type'
    
# Docker toolbox sets an install path environment variable so check for it
$isToolbox = $false
if ($Env:DOCKER_TOOLBOX_INSTALL_PATH) {
    $isToolbox = $true
}

Write-Verbose " => Is Docker Toolbox: $isToolbox"

# TODO: Setup to ensure we have docker machine variables
if ($isToolbox) {

}

# Determine the Docker VM's IP address
Write-Host 'Getting Docker VM IP'
$dockerIpCmd = 'ip -4 addr show scope global dev eth0 | grep inet | awk ''{print $2}'' | cut -d / -f 1'
& docker run --rm --net=host busybox /bin/sh -c $dockerIpCmd 2>&1 | Tee-Object -Variable dockerIp | Out-Null
if ($LastExitCode -ne 0) {
    Write-Host "Could not get Docker VM IP"
    throw $dockerIp
}
Write-Verbose " => Got Docker IP: $dockerIp"

# Determine the VM host's IP address
Write-Host 'Getting Docker VM Host IP'
$hostIpCmd = 'ip -4 route list dev eth0 0/0 | cut -d '' '' -f 3'
& docker run --rm --net=host busybox /bin/sh -c $hostIpCmd 2>&1 | Tee-Object -Variable hostIp | Out-Null
if ($LastExitCode -ne 0) {
    Write-Host "Could not get Docker VM Host IP"
    throw $hostIp
}
Write-Verbose " => Got Host IP: $hostIp"

# Write environment variable pairs to stdout (so this can be piped to a file)
Write-Output "KILLRVIDEO_DOCKER_TOOLBOX=$($isToolbox.ToString().ToLower())"
Write-Output "KILLRVIDEO_HOST_IP=$hostIp"
Write-Output "KILLRVIDEO_DOCKER_IP=$dockerIp"

