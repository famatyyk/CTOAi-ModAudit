-- Przykladowy mod (celowo z bledami do audytu)
local M = {}
function M.on_init()
    -- BLAD: wywoluje powloke (niebezpieczne w modzie)
    os.execute("echo hello")
end
return M
