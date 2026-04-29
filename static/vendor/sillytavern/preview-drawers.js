export const SETTINGS_DRAWER_VENDOR_MARKUP = String.raw`
                <div id="clickSlidersTips" data-i18n="clickslidertips" class="toggle-description wide100p editable-slider-notification">
                    Click slider numbers to input manually.
                </div>
                <div id="labModeWarning" class="redWarningBG textAlignCenter displayNone" data-i18n="MAD LAB MODE ON">MAD LAB MODE ON</div>
                <a class="topRightInset" href="https://docs.sillytavern.app/usage/common-settings/" target="_blank" title="Documentation on sampling parameters." data-i18n="[title]Documentation on sampling parameters">
                    <span name="samplerHelpButton" class="note-link-span fa-solid fa-circle-question"></span>
                </a>
                <div class="scrollableInner">
                    <div class="flex-container flexNoGap" id="ai_response_configuration">
                        <div id="respective-presets-block" class="width100p">
                            <div id="kobold_api-presets">
                                <div class="margin0 title_restorable standoutHeader">
                                    <strong>
                                        <span data-i18n="kobldpresets">Kobold Presets</span>
                                    </strong>

                                    <div class="flex-container gap3px">
                                        <div data-preset-manager-import="kobold" class="margin0 menu_button_icon menu_button" title="Import preset" data-i18n="[title]Import preset">
                                            <i class="fa-fw fa-solid fa-file-import"></i>
                                        </div>
                                        <div data-preset-manager-export="kobold" class="margin0 menu_button_icon menu_button" title="Export preset" data-i18n="[title]Export preset">
                                            <i class="fa-fw fa-solid fa-file-export"></i>
                                        </div>
                                        <div data-preset-manager-delete="kobold" class="margin0 menu_button_icon menu_button" title="Delete the preset" data-i18n="[title]Delete the preset">
                                            <i class="fa-fw fa-solid fa-trash-can"></i>
                                        </div>
                                    </div>
                                </div>
                                <div class="flex-container flexNoGap">
                                    <select id="settings_preset" data-preset-manager-for="kobold" class="flex1 text_pole">
                                        <option value="gui" data-i18n="guikoboldaisettings">GUI KoboldAI Settings</option>
                                    </select>
                                    <div class="flex-container marginLeft5 gap3px">
                                        <input type="file" hidden data-preset-manager-file="kobold" accept=".json, .settings">
                                        <div data-preset-manager-update="kobold" class="menu_button menu_button_icon" title="Update current preset" data-i18n="[title]Update current preset">
                                            <i class="fa-fw fa-solid fa-save"></i>
                                        </div>
                                        <div data-preset-manager-rename="kobold" class="menu_button menu_button_icon" title="Rename current preset" data-i18n="[title]Rename current preset">
                                            <i class="fa-fw fa-solid fa-pencil"></i>
                                        </div>
                                        <div data-preset-manager-new="kobold" class="menu_button menu_button_icon" title="Save preset as" data-i18n="[title]Save preset as">
                                            <i class="fa-fw fa-solid fa-file-circle-plus"></i>
                                        </div>
                                        <div data-preset-manager-restore="kobold" class="menu_button menu_button_icon" title="Restore current preset" data-i18n="[title]Restore current preset">
                                            <i class="fa-fw fa-solid fa-recycle"></i>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div id="common-gen-settings-block" class="width100p">
                            <div id="pro-settings-block" class="flex-container gap10h5v justifyCenter">
                                <div id="amount_gen_block" class="range-block-range-and-counter alignitemscenter flex-container marginBot5 flexFlowColumn flexBasis48p flexGrow flexShrink gap0">
                                    <small data-i18n="response legth(tokens)">Response (tokens)</small>
                                    <input class="neo-range-slider" type="range" id="amount_gen" name="volume" min="16" max="2048" step="1">
                                    <div data-randomization-disabled="true" class="wide100p">
                                        <input class="neo-range-input" type="number" min="16" max="2048" step="1" data-for="amount_gen" id="amount_gen_counter">
                                    </div>
                                    <div id="streaming_textgenerationwebui_block" class="flex-container alignitemscenter justifyCenter marginTop5">
                                        <label class="checkbox_label" for="streaming_textgenerationwebui">
                                            <input type="checkbox" id="streaming_textgenerationwebui" />
                                            <small><span data-i18n="Streaming">Streaming</span>
                                                <div class="margin5 fa-solid fa-circle-info opacity50p" data-i18n="[title]Streaming_desc" title="Display the response bit by bit as it is generated.&#13;When this is off, responses will be displayed all at once when they are complete."></div>
                                            </small>
                                        </label>
                                    </div>
                                    <div id="streaming_kobold_block" class="flex-container alignitemscenter justifyCenter marginTop5">
                                        <label class="checkbox_label" for="streaming_kobold">
                                            <input type="checkbox" id="streaming_kobold" />
                                            <small><span data-i18n="Streaming">Streaming</span>
                                                <div class="margin5 fa-solid fa-circle-info opacity50p" data-i18n="[title]Streaming_desc" title="Display the response bit by bit as it is generated.&#13;When this is off, responses will be displayed all at once when they are complete."></div>
                                            </small>
                                        </label>
                                    </div>
                                    <div id="streaming_novel_block" class="flex-container alignitemscenter justifyCenter marginTop5">
                                        <label class="checkbox_label" for="streaming_novel">
                                            <input type="checkbox" id="streaming_novel" />
                                            <small><span data-i18n="Streaming">Streaming</span>
                                                <div class="margin5 fa-solid fa-circle-info opacity50p" data-i18n="[title]Streaming_desc" title="Display the response bit by bit as it is generated.&#13;When this is off, responses will be displayed all at once when they are complete."></div>
                                            </small>
                                        </label>
                                    </div>
                                </div>
                                <div id="max_context_block" class="range-block-range-and-counter alignitemscenter flex-container marginBot5 flexFlowColumn flexBasis48p flexGrow flexShrink gap0">
                                    <small data-i18n="context size(tokens)">Context (tokens)</small>
                                    <input class="neo-range-slider" type="range" id="max_context" name="volume" min="512" max="8192" step="64">
                                    <div data-randomization-disabled="true" class="wide100p">
                                        <input class="neo-range-input" type="number" min="512" max="8192" step="64" data-for="max_context" id="max_context_counter">
                                    </div>
                                    <div class="flex-container alignitemscenter justifyCenter marginTop5" id="max_context_unlocked_block">
                                        <label class="checkbox_label">
                                            <input id="max_context_unlocked" type="checkbox" />
                                            <small><span data-i18n="unlocked">Unlocked</span>
                                                <div id="max_context_unlocked_warning" class="fa-solid fa-circle-info opacity50p " data-i18n="[title]Only enable this if your model supports context sizes greater than 8192 tokens" title="Only enable this if your model supports context sizes greater than 8192 tokens.&#13;Increase only if you know what you're doing."></div>
                                            </small>
                                        </label>
                                    </div>
                                </div>
                                <small id="prompt_cost_block" data-tg-type="openrouter">
                                    <span data-i18n="Max prompt cost:">Max prompt cost:</span> <span id="or_prompt_cost">&ndash;</span>
                                </small>
                            </div>
                            <div id="ai_module_block_novel" class="width100p">
                                <div class="range-block">
                                    <div class="range-block-title justifyLeft" data-i18n="AI Module">
                                        AI Module
                                    </div>
                                    <div class="toggle-description justifyLeft" data-i18n="Changes the style of the generated text.">
                                        Changes the style of the generated text.
                                    </div>
                                    <select id="nai_prefix">
                                        <option value="vanilla" data-i18n="No Module">No Module</option>
                                        <option value="special_instruct" data-i18n="Instruct">Instruct</option>
                                        <option value="special_proseaugmenter" data-i18n="Prose Augmenter">Prose Augmenter</option>
                                        <option value="theme_textadventure" data-i18n="Text Adventure">Text Adventure</option>
                                    </select>
                                </div>
                            </div>
                            <hr>
                        </div>
                        <div id="advanced-ai-config-block" class="width100p">
                            <div id="kobold_api-settings">
                                <div class="flex-container gap10h5v justifyCenter">
                                    <div class="alignitemscenter flex-container flexFlowColumn flexBasis30p flexGrow flexShrink gap0">
                                        <small>
                                            <span data-i18n="Temperature">Temperature</span>
                                            <div class="fa-solid fa-circle-info opacity50p" data-i18n="[title]Temperature controls the randomness in token selection" title="Temperature controls the randomness in token selection:&#13;- low temperature (<1.0) leads to more predictable text, favoring higher probability tokens.&#13;- high temperature (>1.0) increases creativity and diversity in the output by giving lower probability tokens a better chance.&#13;Set to 1.0 for the original probabilities."></div>
                                        </small>
                                        <input class="neo-range-slider" type="range" id="temp" name="volume" min="0.0" max="4.0" step="0.01">
                                        <input class="neo-range-input" type="number" min="0.0" max="4.0" step="0.01" data-for="temp" id="temp_counter">
                                    </div>
                                    <div class="alignitemscenter flex-container flexFlowColumn flexBasis30p flexGrow flexShrink gap0">
                                        <small>
                                            <span data-i18n="Top K">Top K</span>
                                            <div class="fa-solid fa-circle-info opacity50p" title="Top K sets a maximum amount of top tokens that can be chosen from.&#13;E.g Top K is 20, this means only the 20 highest ranking tokens will be kept (regardless of their probabilities being diverse or limited).&#13;Set to 0 to disable." data-i18n="[title]Top_K_desc"></div>
                                        </small>
                                        <input class="neo-range-slider" type="range" id="top_k" name="volume" min="0" max="100" step="1">
                                        <input class="neo-range-input" type="number" min="0" max="100" step="1" data-for="top_k" id="top_k_counter">
                                    </div>
                                    <div class="alignitemscenter flex-container flexFlowColumn flexBasis30p flexGrow flexShrink gap0">
                                        <small>
                                            Top P
                                            <div class="fa-solid fa-circle-info opacity50p" title="Top P (a.k.a. nucleus sampling) adds up all the top tokens required to add up to the target percentage.&#13;E.g If the Top 2 tokens are both 25%, and Top P is 0.50, only the Top 2 tokens are considered.&#13;Set to 1.0 to disable." data-i18n="[title]Top_P_desc"></div>
                                        </small>
                                        <input class="neo-range-slider" type="range" id="top_p" name="volume" min="0" max="1" step="0.01">
                                        <input class="neo-range-input" type="number" min="0" max="1" step="0.01" data-for="top_p" id="top_p_counter">
                                    </div>
                                    <div class="alignitemscenter flex-container flexFlowColumn flexBasis30p flexGrow flexShrink gap0">
                                        <small>
                                            <span data-i18n="Typical P">Typical P</span>
                                            <div class="fa-solid fa-circle-info opacity50p" title="Typical P Sampling prioritizes tokens based on their deviation from the average entropy of the set.&#13;It maintains tokens whose cumulative probability is close to a predefined threshold (e.g., 0.5), emphasizing those with average information content.&#13;Set to 1.0 to disable." data-i18n="[title]Typical_P_desc"></div>
                                        </small>
                                        <input class="neo-range-slider" type="range" id="typical_p" name="volume" min="0" max="1" step="0.001">
                                        <input class="neo-range-input" type="number" min="0" max="1" step="0.001" data-for="typical_p" id="typical_p_counter">
                                    </div>
                                    <div class="alignitemscenter flex-container flexFlowColumn flexBasis30p flexGrow flexShrink gap0">
                                        <small>
                                            <span data-i18n="Min P">Min P</span>
                                            <div class="fa-solid fa-circle-info opacity50p" title="Min P sets a base minimum probability.&#13;This is scaled according to the top token's probability.&#13;E.g If Top token is 80% probability, and Min P is 0.1, only tokens higher than 8% would be considered.&#13;Set to 0 to disable." data-i18n="[title]Min_P_desc"></div>
                                        </small>
                                        <input class="neo-range-slider" type="range" id="min_p" name="volume" min="0" max="1" step="0.001">
                                        <input class="neo-range-input" type="number" min="0" max="1" step="0.001" data-for="min_p" id="min_p_counter">
                                    </div>
                                    <div class="alignitemscenter flex-container flexFlowColumn flexBasis30p flexGrow flexShrink gap0">
                                        <small>
                                            <span data-i18n="Top A">Top A</span>
                                            <div class="fa-solid fa-circle-info opacity50p" title="Top A sets a threshold for token selection based on the square of the highest token probability.&#13;E.g if the Top-A value is 0.2 and the top token's probability is 50%, tokens with probabilities below 5% (0.2 * 0.5^2) are excluded.&#13;Set to 0 to disable." data-i18n="[title]Top_A_desc"></div>
                                        </small>
                                        <input class="neo-range-slider" type="range" id="top_a" name="volume" min="0" max="1" step="0.001">
                                        <input class="neo-range-input" type="number" min="0" max="1" step="0.001" data-for="top_a" id="top_a_counter">
                                    </div>
                                    <div class="alignitemscenter flex-container flexFlowColumn flexBasis30p flexGrow flexShrink gap0">
                                        <small>
                                            <span data-i18n="TFS">TFS</span>
                                            <div class="fa-solid fa-circle-info opacity50p" title="Tail-Free Sampling (TFS) searches for a tail of low-probability tokens in the distribution,&#13;by analyzing the rate of change in token probabilities using derivatives. It retains tokens up to a threshold (e.g., 0.3) based on the normalized second derivative.&#13;The closer to 0, the more discarded tokens. Set to 1.0 to disable." data-i18n="[title]Tail_Free_Sampling_desc"></div>
                                        </small>
                                        <input class="neo-range-slider" type="range" id="tfs" name="volume" min="0" max="1" step="0.001">
                                        <input class="neo-range-input" type="number" min="0" max="1" step="0.001" data-for="tfs" id="tfs_counter">
                                    </div>
                                    <div class="alignitemscenter flex-container flexFlowColumn flexBasis30p flexGrow flexShrink gap0">
                                        <small>
                                            <span data-i18n="rep.pen">Repetition Penalty</span>
                                        </small>
                                        <input class="neo-range-slider" type="range" id="rep_pen" name="volume" min="1" max="3" step="0.01">
                                        <input class="neo-range-input" type="number" min="1" max="3" step="0.01" data-for="rep_pen" id="rep_pen_counter">
                                    </div>
                                    <div class="alignitemscenter flex-container flexFlowColumn flexBasis30p flexGrow flexShrink gap0">
                                        <small>
                                            <span data-i18n="rep.pen range">Rep Pen Range</span>
                                        </small>
                                        <input class="neo-range-slider" type="range" id="rep_pen_range" name="volume" min="0" max="4096" step="1">
                                        <input class="neo-range-input" type="number" min="0" max="4096" step="1" data-for="rep_pen_range" id="rep_pen_range_counter">
                                    </div>
                                    <div class="alignitemscenter flex-container flexFlowColumn flexBasis30p flexGrow flexShrink gap0">
                                        <small>
                                            <span data-i18n="Rep. Pen. Slope">Repetition Penalty Slope</span>
                                        </small>
                                        <input class="neo-range-slider" type="range" id="rep_pen_slope" name="volume" min="0" max="10" step="0.01">
                                        <input class="neo-range-input" type="number" min="0" max="10" step="0.01" data-for="rep_pen_slope" id="rep_pen_slope_counter">
                                    </div>
                                    <div name="miroStatBlock-kobold" class="wide100p">
                                        <h4 class="wide100p textAlignCenter" data-i18n="Mirostat">Mirostat</h4>
                                        <div class="flex-container flexFlowRow gap10px flexShrink">
                                            <div class="alignitemscenter flex-container flexFlowColumn flexGrow flexShrink gap0">
                                                <small>
                                                    <span data-i18n="Mode">Mode</span>
                                                    <div class="fa-solid fa-circle-info opacity50p" title="A value of 0 disables Mirostat entirely. 1 is for Mirostat 1.0, and 2 is for Mirostat 2.0" data-i18n="[title]Mirostat_Mode_desc"></div>
                                                </small>
                                                <input class="neo-range-slider" type="range" id="mirostat_mode_kobold" name="volume" min="0" max="2" step="1" />
                                                <input class="neo-range-input" type="number" min="0" max="2" step="1" data-for="mirostat_mode_kobold" id="mirostat_mode_counter_kobold">
                                            </div>
                                            <div class="alignitemscenter flex-container flexFlowColumn flexGrow flexShrink gap0">
                                                <small>
                                                    <span data-i18n="Tau">Tau</span>
                                                    <div class="fa-solid fa-circle-info opacity50p" title="Controls variability of Mirostat outputs" data-i18n="[title]Mirostat_Tau_desc"></div>
                                                </small>
                                                <input class="neo-range-slider" type="range" id="mirostat_tau_kobold" name="volume" min="0" max="20" step="0.01" />
                                                <input class="neo-range-input" type="number" min="0" max="20" step="0.01" data-for="mirostat_tau_kobold" id="mirostat_tau_counter_kobold">
                                            </div>
                                            <div class="alignitemscenter flex-container flexFlowColumn flexGrow flexShrink gap0">
                                                <small>
                                                    <span data-i18n="Eta">Eta</span>
                                                    <div class="fa-solid fa-circle-info opacity50p" title="Controls learning rate of Mirostat" data-i18n="[title]Mirostat_Eta_desc"></div>
                                                </small>
                                                <input class="neo-range-slider" type="range" id="mirostat_eta_kobold" name="volume" min="0" max="1" step="0.01" />
                                                <input class="neo-range-input" type="number" min="0" max="1" step="0.01" data-for="mirostat_eta_kobold" id="mirostat_eta_counter_kobold">
                                            </div>
                                        </div>
                                        <hr class="wide100p">
                                    </div>
                                    <div class="alignitemscenter justifyCenter flex-container flexFlowColumn flexBasis30p flexGrow flexShrink gap0">
                                        <label class="checkbox_label alignItemsBaseline" for="use_default_badwordsids">
                                            <input id="use_default_badwordsids" type="checkbox" />
                                            <span>
                                                <span data-i18n="Ban EOS Token">Ban EOS Token</span>
                                                <small class="fa-solid fa-circle-info opacity50p" title="Ban the End-of-Sequence (EOS) token with KoboldCpp (and possibly also other tokens with KoboldAI).&#13;Good for story writing, but should not be used for chat and instruct mode." data-i18n="[title]Ban_EOS_Token_desc"></small>
                                            </span>
                                        </label>
                                    </div>
                                    <div class="alignitemscenter textAlignCenter flexBasis30p flexGrow flexShrink gap0">
                                        <!-- <hr class="wide100p"> -->
                                        <small data-i18n="Seed">Seed</small>
                                        <!-- Max value is 2**64 - 1 -->
                                        <input type="number" id="seed_kobold" class="text_pole wideMax100px" min="-1" value="-1" max="18446744073709551615" />
                                    </div>
                                    <div id="grammar_block" class="wide100p">
                                        <hr class="wide100p">
                                        <h4 class="wide100p textAlignCenter"><span data-i18n="GBNF Grammar">GBNF Grammar</span>
                                            <a href="https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md" target="_blank">
                                                <small>
                                                    <div class="fa-solid fa-circle-question note-link-span"></div>
                                                </small>
                                            </a>
                                        </h4>
                                        <textarea id="grammar" rows="4" class="text_pole textarea_compact monospace" data-i18n="[placeholder]Type in the desired custom grammar" placeholder="Type in the desired custom grammar"></textarea>
                                    </div>
                                    <div name="KoboldSamplerOrderBlock" class="range-block flexFlowColumn">
                                        <hr class="wide100p">
                                        <div class="range-block-title">
                                            <span data-i18n="Samplers Order">Samplers Order</span>
                                        </div>
                                        <div class="toggle-description widthUnset" data-i18n="Samplers will be applied in a top-down order. Use with caution.">
                                            Samplers will be applied in a top-down order.
                                            Use with caution.
                                        </div>
                                        <div id="kobold_order" class="prompt_order">
                                            <div data-id="0">
                                                <span data-i18n="Top K">Top K</span>
                                                <small>0</small>
                                            </div>
                                            <div data-id="1">
                                                <span data-i18n="Top A">Top A</span>
                                                <small>1</small>
                                            </div>
                                            <div data-id="2">
                                                <span data-i18n="Top P">Top P & Min P</span>
                                                <small>2</small>
                                            </div>
                                            <div data-id="3">
                                                <span data-i18n="Tail Free Sampling">Tail Free Sampling</span>
                                                <small>3</small>
                                            </div>
                                            <div data-id="4">
                                                <span data-i18n="Typical P">Typical P</span>
                                                <small>4</small>
                                            </div>
                                            <div data-id="5">
                                                <span data-i18n="Temperature">Temperature</span>
                                                <small>5</small>
                                            </div>
                                            <div data-id="6">
                                                <span data-i18n="Repetition Penalty">Repetition Penalty</span>
                                                <small>6</small>
                                            </div>
                                        </div>
                                        <div id="samplers_order_recommended" class="menu_button menu_button_icon">
                                            <span data-i18n="Load koboldcpp order">Load koboldcpp order</span>
                                        </div>
                                    </div>
                                </div>
                            </div><!-- end of kobold settings-->
                        </div>
                    </div>
                </div>`;

export const FORMATTING_DRAWER_VENDOR_MARKUP = String.raw`
                <div class="flex-container alignItemsBaseline">
                    <h3 class="margin0 flex1 flex-container alignItemsBaseline">
                        <span data-i18n="Advanced Formatting">
                            Advanced Formatting
                        </span>

                        <a href="https://docs.sillytavern.app/usage/core-concepts/advancedformatting/" class="notes-link" target="_blank">
                            <span class="fa-solid fa-circle-question note-link-span"></span>
                        </a>
                    </h3>
                    <div class="flex-container" data-cc-null>
                        <input id="af_master_import_file" type="file" hidden accept=".json" class="displayNone">
                        <div id="af_master_import" class="menu_button menu_button_icon" title="Import Advanced Formatting settings&#10;&#10;You can also provide legacy files for Instruct and Context templates." data-i18n="[title]Import Advanced Formatting settings">
                            <i class="fa-solid fa-file-import"></i>
                            <span data-i18n="Master Import">Master Import</span>
                        </div>
                        <div id="af_master_export" class="menu_button menu_button_icon" title="Export Advanced Formatting settings" data-i18n="[title]Export Advanced Formatting settings">
                            <i class="fa-solid fa-file-export"></i>
                            <span data-i18n="Master Export">Master Export</span>
                        </div>
                    </div>
                </div>
                <div id="advanced-formatting-cc-notice" class="info-block warning">
                    <i class="fa-solid fa-triangle-exclamation"></i>
                    <span data-i18n="Grayed-out options have no effect when Chat Completion API is used.">
                        Grayed-out options have no effect when Chat Completion API is used.
                    </span>
                </div>
                <div class="flex-container spaceEvenly">
                    <div id="ContextSettings" class="flex-container flexNoGap flexFlowColumn flex1">
                        <div>
                            <h4 class="standoutHeader title_restorable" data-cc-null>
                                <div>
                                    <span data-i18n="Context Template">Context Template</span>
                                </div>
                                <div class="flex-container">
                                    <label for="context_derived" class="checkbox_label flex1" title="Derive from Model Metadata, if possible." data-i18n="[title]context_derived">
                                        <input id="context_derived" type="checkbox" style="display:none;" />
                                        <small><i class="fa-solid fa-bolt menu_button margin0"></i></small>
                                    </label>
                                </div>
                            </h4>
                            <div class="flex-container" title="Select your current Context Template" data-i18n="[title]Select your current Context Template" data-cc-null>
                                <select id="context_presets" data-preset-manager-for="context" class="flex1 text_pole"></select>
                                <div class="flex-container justifyCenter gap3px">
                                    <input type="file" hidden data-preset-manager-file="context" accept=".json, .settings">
                                    <i data-preset-manager-update="context" class="menu_button fa-solid fa-save" title="Update current template" data-i18n="[title]Update current template"></i>
                                    <i data-preset-manager-rename="context" class="menu_button fa-pencil fa-solid" title="Rename current template" data-i18n="[title]Rename current template"></i>
                                    <i data-preset-manager-new="context" class="menu_button fa-solid fa-file-circle-plus" title="Save template as" data-i18n="[title]Save template as"></i>
                                    <i data-preset-manager-import="context" class="displayNone menu_button fa-solid fa-file-import" title="Import template" data-i18n="[title]Import template"></i>
                                    <i data-preset-manager-export="context" class="displayNone menu_button fa-solid fa-file-export" title="Export template" data-i18n="[title]Export template"></i>
                                    <i data-preset-manager-restore="context" class="menu_button fa-solid fa-recycle" title="Restore current template" data-i18n="[title]Restore current template"></i>
                                    <i id="context_delete_preset" data-preset-manager-delete="context" class="menu_button fa-solid fa-trash-can" title="Delete the template" data-i18n="[title]Delete the template"></i>
                                </div>
                            </div>
                            <div>
                                <div data-cc-null>
                                    <label for="context_story_string" class="flex-container">
                                        <small data-i18n="Story String">Story String</small>
                                        <i class="editor_maximize fa-solid fa-maximize right_menu_button" data-for="context_story_string" title="Expand the editor" data-i18n="[title]Expand the editor"></i>
                                    </label>
                                    <textarea id="context_story_string" data-macros class="text_pole textarea_compact autoSetHeight"></textarea>
                                </div>
                                <div class="flex-container flexFlowColumn" data-cc-null>
                                    <div id="context_story_string_position_block">
                                        <label for="context_story_string_position">
                                            <small data-i18n="Position:">Position:</small>
                                        </label>
                                        <select id="context_story_string_position" class="text_pole">
                                            <option value="0" data-i18n="Default (top of context)">Default (top of context)</option>
                                            <option value="1" data-i18n="In-chat @ Depth">In-chat @ Depth</option>
                                        </select>
                                    </div>
                                    <div id="context_story_string_inject_settings" class="flex-container">
                                        <div class="flex1">
                                            <label for="context_story_string_depth">
                                                <small data-i18n="Depth:">Depth:</small>
                                            </label>
                                            <input type="number" id="context_story_string_depth" class="text_pole" min="0" max="">
                                        </div>
                                        <div class="flex1">
                                            <label for="context_story_string_role">
                                                <small data-i18n="Role:">Role:</small>
                                            </label>
                                            <select id="context_story_string_role" class="text_pole">
                                                <option data-i18n="System" value="0">System</option>
                                                <option data-i18n="User" value="1">User</option>
                                                <option data-i18n="Assistant" value="2">Assistant</option>
                                            </select>
                                        </div>
                                    </div>
                                </div>
                                <div class="flex-container" data-cc-null>
                                    <div class="flex1">
                                        <label for="context_example_separator">
                                            <small data-i18n="Example Separator">Example Separator</small>
                                        </label>
                                        <div>
                                            <textarea id="context_example_separator" data-macros class="text_pole textarea_compact autoSetHeight"></textarea>
                                        </div>
                                    </div>
                                    <div class="flex1">
                                        <label for="context_chat_start">
                                            <small data-i18n="Chat Start">Chat Start</small>
                                        </label>
                                        <div>
                                            <textarea id="context_chat_start" data-macros class="text_pole textarea_compact autoSetHeight"></textarea>
                                        </div>
                                    </div>
                                </div>
                                <div>
                                    <h4 class="standoutHeader">
                                        <span data-i18n="Context Formatting">
                                            Context Formatting
                                        </span>
                                    </h4>

                                    <label class="checkbox_label" for="always-force-name2-checkbox" data-cc-null>
                                        <input id="always-force-name2-checkbox" type="checkbox" />
                                        <small data-i18n="Always add character's name to prompt">
                                            Always add character's name to prompt
                                        </small>
                                    </label>
                                    <label class="checkbox_label" for="single_line" data-cc-null>
                                        <input id="single_line" type="checkbox" />
                                        <small data-i18n="Generate only one line per request">
                                            Generate only one line per request
                                        </small>
                                    </label>
                                    <label class="checkbox_label" for="collapse-newlines-checkbox">
                                        <input id="collapse-newlines-checkbox" type="checkbox" />
                                        <small data-i18n="Collapse Consecutive Newlines">
                                            Collapse Consecutive Newlines
                                        </small>
                                    </label>
                                    <label class="checkbox_label" for="trim_spaces">
                                        <input id="trim_spaces" type="checkbox" />
                                        <small data-i18n="Trim spaces">Trim spaces</small>
                                        <i class="fa-sm fa-solid fa-exclamation-triangle warning" title="Disabling is not recommended." data-i18n="[title]Disabling is not recommended."></i>
                                    </label>
                                    <label class="checkbox_label" for="trim_sentences_checkbox">
                                        <input id="trim_sentences_checkbox" type="checkbox" />
                                        <small data-i18n="Trim Incomplete Sentences">
                                            Trim Incomplete Sentences
                                        </small>
                                    </label>
                                    <label class="checkbox_label" title="Add Chat Start and Example Separator to a list of stopping strings." data-i18n="[title]Add Chat Start and Example Separator to a list of stopping strings." data-cc-null>
                                        <input id="context_use_stop_strings" type="checkbox" />
                                        <small data-i18n="Separators as Stop Strings">Separators as Stop Strings</small>
                                    </label>
                                    <label class="checkbox_label" title="Add Character and User names to a list of stopping strings." data-i18n="[title]Add Character and User names to a list of stopping strings." data-cc-null>
                                        <input id="context_names_as_stop_strings" type="checkbox" />
                                        <small data-i18n="Names as Stop Strings">Names as Stop Strings</small>
                                    </label>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div id="InstructSettingsColumn" class="flex-container flexNoGap flexFlowColumn flex1" data-cc-null>
                        <h4 class="standoutHeader title_restorable justifySpaceBetween">
                            <div class="flex-container">
                                <span data-i18n="Instruct Template">Instruct Template</span>
                            </div>
                            <div class="flex-container">
                                <label for="instruct_derived" class="checkbox_label flex1" title="Derive from Model Metadata, if possible." data-i18n="[title]instruct_derived">
                                    <input id="instruct_derived" type="checkbox" style="display:none;" />
                                    <small><i class="fa-solid fa-bolt menu_button margin0"></i></small>
                                </label>
                                <label for="instruct_bind_to_context" class="checkbox_label flex1" title="Bind to Context&#10;If enabled, Context templates will be automatically selected based on selected Instruct template name or by preference." data-i18n="[title]instruct_bind_to_context">
                                    <input id="instruct_bind_to_context" type="checkbox" style="display:none;" />
                                    <small><i class="fa-solid fa-link menu_button margin0"></i></small>
                                </label>
                                <label id="instruct_enabled_label" for="instruct_enabled" class="checkbox_label flex1" title="Enable Instruct Mode" data-i18n="[title]instruct_enabled">
                                    <input id="instruct_enabled" type="checkbox" style="display:none;" />
                                    <small><i class="fa-solid fa-power-off menu_button togglable margin0"></i></small>
                                </label>
                            </div>
                        </h4>
                        <div id="instructSettingsBlock">


                            <div class="flex-container" title="Select your current Instruct Template" data-i18n="[title]Select your current Instruct Template">
                                <select id="instruct_presets" data-preset-manager-for="instruct" class="flex1 text_pole"></select>
                                <div class="flex-container margin0 justifyCenter gap3px">
                                    <input type="file" hidden data-preset-manager-file="instruct" accept=".json, .settings">
                                    <i data-preset-manager-update="instruct" class="menu_button fa-solid fa-save" title="Update current template" data-i18n="[title]Update current template"></i>
                                    <i data-preset-manager-rename="instruct" class="menu_button fa-pencil fa-solid" title="Rename current template" data-i18n="[title]Rename current template"></i>
                                    <i data-preset-manager-new="instruct" class="menu_button fa-solid fa-file-circle-plus" title="Save template as" data-i18n="[title]Save template as"></i>
                                    <i data-preset-manager-import="instruct" class="displayNone menu_button fa-solid fa-file-import" title="Import template" data-i18n="[title]Import template"></i>
                                    <i data-preset-manager-export="instruct" class="displayNone menu_button fa-solid fa-file-export" title="Export template" data-i18n="[title]Export template"></i>
                                    <i data-preset-manager-restore="instruct" class="menu_button fa-solid fa-recycle" title="Restore current template" data-i18n="[title]Restore current template"></i>
                                    <i data-preset-manager-delete="instruct" class="menu_button fa-solid fa-trash-can" title="Delete template" data-i18n="[title]Delete template"></i>
                                </div>
                            </div>
                            <label>
                                <small>
                                    <span data-i18n="Activation Regex">Activation Regex</span>
                                    <span class="fa-solid fa-circle-question" data-i18n="[title]instruct_template_activation_regex_desc" title="When connecting to an API or choosing a model, automatically activate this Instruct Template if the model name matches the provided regular expression."></span>
                                </small>
                            </label>
                            <div>
                                <input type="text" id="instruct_activation_regex" class="text_pole textarea_compact" placeholder="e.g. /llama(-)?[3|3.1]/i">
                            </div>
                            <div>
                                <label for="instruct_wrap" class="checkbox_label">
                                    <input id="instruct_wrap" type="checkbox" />
                                    <small data-i18n="Wrap Sequences with Newline">Wrap Sequences with Newline</small>
                                </label>
                                <label for="instruct_macro" class="checkbox_label">
                                    <input id="instruct_macro" type="checkbox" />
                                    <small data-i18n="Replace Macro in Sequences">Replace Macro in Sequences</small>
                                </label>
                                <label for="instruct_sequences_as_stop_strings" class="checkbox_label">
                                    <input id="instruct_sequences_as_stop_strings" type="checkbox" />
                                    <small data-i18n="Sequences as Stop Strings">Sequences as Stop Strings</small>
                                </label>
                                <label for="instruct_skip_examples" class="checkbox_label">
                                    <input id="instruct_skip_examples" type="checkbox" />
                                    <small data-i18n="Skip Example Dialogues Formatting">Skip Example Dialogues Formatting</small>
                                </label>
                                <div>
                                    <small data-i18n="Include Names">
                                        Include Names
                                    </small>
                                    <select id="instruct_names_behavior">
                                        <option value="none" data-i18n="Never">Never</option>
                                        <option value="force" data-i18n="Groups and Past Personas">Groups and Past Personas</option>
                                        <option value="always" data-i18n="Always">Always</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        <div id="InstructSequencesColumn" class="wide100p flexFlowColumn">
                            <h4 class="standoutHeader title_restorable">
                                <b>
                                    <span data-i18n="Instruct Sequences">
                                        Instruct Sequences
                                    </span>
                                </b>
                            </h4>
                            <!-- We keep some auto-open so the user would know what is going on in the picked template -->
                            <details open>
                                <summary>
                                    <span data-i18n="Story String Sequences">Story String Sequences</span>
                                    <small class="fa-solid fa-question-circle" title="Used in Default position only." data-i18n="[title]Used in Default position only."></small>
                                </summary>
                                <div class="flex-container">
                                    <div class="flexAuto" title="Inserted before a Story String." data-i18n="[title]Inserted before a Story String.">
                                        <label for="instruct_story_string_prefix">
                                            <small data-i18n="Story String Prefix">Story String Prefix</small>
                                        </label>
                                        <div>
                                            <textarea id="instruct_story_string_prefix" class="text_pole textarea_compact autoSetHeight"></textarea>
                                        </div>
                                    </div>
                                    <div class="flexAuto" title="Inserted after a Story String." data-i18n="[title]Inserted after a Story String.">
                                        <label for="instruct_story_string_suffix">
                                            <small data-i18n="Story String Suffix">Story String Suffix</small>
                                        </label>
                                        <div>
                                            <textarea id="instruct_story_string_suffix" class="text_pole wide100p textarea_compact autoSetHeight"></textarea>
                                        </div>
                                    </div>
                                </div>
                            </details>
                            <details open>
                                <summary data-i18n="User Message Sequences">User Message Sequences</summary>
                                <div class="flex-container">
                                    <div class="flexAuto" title="Inserted before a User message and as a last prompt line when impersonating." data-i18n="[title]Inserted before a User message and as a last prompt line when impersonating.">
                                        <small data-i18n="User Prefix">User Message Prefix</small>
                                        <textarea id="instruct_input_sequence" data-macros class="text_pole textarea_compact autoSetHeight"></textarea>
                                    </div>
                                    <div class="flexAuto" title="Inserted after a User message." data-i18n="[title]Inserted after a User message.">
                                        <small data-i18n="User Suffix">User Message Suffix</small>
                                        <textarea id="instruct_input_suffix" data-macros class="text_pole wide100p textarea_compact autoSetHeight"></textarea>
                                    </div>
                                </div>
                            </details>
                            <details open>
                                <summary data-i18n="Assistant Message Sequences">Assistant Message Sequences</summary>
                                <div class="flex-container">
                                    <div class="flexAuto" title="Inserted before an Assistant message and as a last prompt line when generating an AI reply." data-i18n="[title]Inserted before an Assistant message and as a last prompt line when generating an AI reply.">
                                        <small data-i18n="Assistant Prefix">Assistant Message Prefix</small>
                                        <textarea id="instruct_output_sequence" data-macros class="text_pole wide100p textarea_compact autoSetHeight"></textarea>
                                    </div>
                                    <div class="flexAuto" title="Inserted after an Assistant message." data-i18n="[title]Inserted after an Assistant message.">
                                        <small data-i18n="Assistant Suffix">Assistant Message Suffix</small>
                                        <textarea id="instruct_output_suffix" data-macros class="text_pole wide100p textarea_compact autoSetHeight"></textarea>
                                    </div>
                                </div>
                            </details>
                            <details>
                                <summary data-i18n="System Message Sequences">System Message Sequences</summary>
                                <div class="flex-container">
                                    <div class="flexAuto" id="instruct_system_sequence_block" title="Inserted before a System (added by slash commands or extensions) message." data-i18n="[title]Inserted before a System (added by slash commands or extensions) message.">
                                        <small data-i18n="System Prefix">System Message Prefix</small>
                                        <textarea id="instruct_system_sequence" data-macros class="text_pole textarea_compact autoSetHeight"></textarea>
                                    </div>
                                    <div class="flexAuto" id="instruct_system_suffix_block" title="Inserted after a System message." data-i18n="[title]Inserted after a System message.">
                                        <small data-i18n="System Suffix">System Message Suffix</small>
                                        <textarea id="instruct_system_suffix" data-macros class="text_pole wide100p textarea_compact autoSetHeight"></textarea>
                                    </div>
                                </div>
                                <div class="flexBasis100p" title="If enabled, System Sequences will be the same as User Sequences." data-i18n="[title]If enabled, System Sequences will be the same as User Sequences.">
                                    <label class="checkbox_label" for="instruct_system_same_as_user">
                                        <input id="instruct_system_same_as_user" type="checkbox" />
                                        <small data-i18n="System same as User">System same as User</small>
                                    </label>
                                </div>
                            </details>
                            <details>
                                <summary data-i18n="Misc. Sequences">Misc. Sequences</summary>
                                <div class="flex-container">
                                    <div class="flexAuto" title="Inserted before the first Assistant's message." data-i18n="[title]Inserted before the first Assistant's message.">
                                        <small data-i18n="First Assistant Prefix">First Assistant Prefix</small>
                                        <textarea id="instruct_first_output_sequence" data-macros class="text_pole textarea_compact autoSetHeight"></textarea>
                                    </div>
                                    <div class="flexAuto" title="Inserted before the last Assistant's message or as a last prompt line when generating an AI reply (except a neutral/system role)." data-i18n="[title]instruct_last_output_sequence">
                                        <small data-i18n="Last Assistant Prefix">Last Assistant Prefix</small>
                                        <textarea id="instruct_last_output_sequence" data-macros class="text_pole wide100p textarea_compact autoSetHeight"></textarea>
                                    </div>
                                </div>
                                <div class="flex-container">
                                    <div class="flexAuto" title="Inserted before the first User's message." data-i18n="[title]Inserted before the first User's message.">
                                        <small data-i18n="First User Prefix">First User Prefix</small>
                                        <textarea id="instruct_first_input_sequence" data-macros class="text_pole textarea_compact autoSetHeight"></textarea>
                                    </div>
                                    <div class="flexAuto" title="Inserted before the last User's message." data-i18n="[title]instruct_last_input_sequence">
                                        <small data-i18n="Last User Prefix">Last User Prefix</small>
                                        <textarea id="instruct_last_input_sequence" data-macros class="text_pole wide100p textarea_compact autoSetHeight"></textarea>
                                    </div>
                                </div>
                                <div class="flex-container">
                                    <div class="flexAuto" title="Will be inserted as a last prompt line when using system/neutral generation." data-i18n="[title]Will be inserted as a last prompt line when using system/neutral generation.">
                                        <small data-i18n="System Instruction Prefix">System Instruction Prefix</small>
                                        <textarea id="instruct_last_system_sequence" data-macros class="text_pole textarea_compact autoSetHeight"></textarea>
                                    </div>
                                    <div class="flexAuto" title="If a stop sequence is generated, everything past it will be removed from the output (inclusive)." data-i18n="[title]If a stop sequence is generated, everything past it will be removed from the output (inclusive).">
                                        <small data-i18n="Stop Sequence">Stop Sequence</small>
                                        <textarea id="instruct_stop_sequence" data-macros class="text_pole textarea_compact autoSetHeight"></textarea>
                                    </div>
                                </div>
                                <div class="flex-container">
                                    <div class="flexAuto" title="Will be inserted at the start of the chat history if it doesn't start with a User message." data-i18n="[title]Will be inserted at the start of the chat history if it doesn't start with a User message.">
                                        <small data-i18n="User Filler Message">User Filler Message</small>
                                        <textarea id="instruct_user_alignment_message" data-macros class="text_pole textarea_compact autoSetHeight"></textarea>
                                    </div>
                                </div>
                            </details>
                        </div>
                    </div>
                    <div id="SystemPromptColumn" class="flex-container flexNoGap flexFlowColumn flex1">
                        <h4 class="standoutHeader title_restorable justifySpaceBetween" data-cc-null>
                            <div class="flex-container">
                                <span data-i18n="System Prompt">System Prompt</span>
                            </div>
                            <div class="flex-container">
                                <label id="sysprompt_enabled_label" for="sysprompt_enabled" class="checkbox_label flex1" title="Enable System Prompt" data-i18n="[title]sysprompt_enabled">
                                    <input id="sysprompt_enabled" type="checkbox" style="display:none;" />
                                    <small><i class="fa-solid fa-power-off menu_button togglable margin0"></i></small>
                                </label>
                            </div>
                        </h4>
                        <div id="SystemPromptBlock" class="marginBot10" data-cc-null>
                            <div class="flex-container" title="Select your current System Prompt" data-i18n="[title]Select your current System Prompt">
                                <select id="sysprompt_select" data-preset-manager-for="sysprompt" class="flex1 text_pole"></select>
                                <div class="flex-container margin0 justifyCenter gap3px">
                                    <input type="file" hidden data-preset-manager-file="sysprompt" accept=".json, .settings">
                                    <i data-preset-manager-update="sysprompt" class="menu_button fa-solid fa-save" title="Update current prompt" data-i18n="[title]Update current prompt"></i>
                                    <i data-preset-manager-rename="sysprompt" class="menu_button fa-pencil fa-solid" title="Rename current prompt" data-i18n="[title]Rename current prompt"></i>
                                    <i data-preset-manager-new="sysprompt" class="menu_button fa-solid fa-file-circle-plus" title="Save prompt as" data-i18n="[title]Save prompt as"></i>
                                    <i data-preset-manager-import="sysprompt" class="displayNone menu_button fa-solid fa-file-import" title="Import template" data-i18n="[title]Import template"></i>
                                    <i data-preset-manager-export="sysprompt" class="displayNone menu_button fa-solid fa-file-export" title="Export template" data-i18n="[title]Export template"></i>
                                    <i data-preset-manager-restore="sysprompt" class="menu_button fa-solid fa-recycle" title="Restore current prompt" data-i18n="[title]Restore current prompt"></i>
                                    <i data-preset-manager-delete="sysprompt" class="menu_button fa-solid fa-trash-can" title="Delete prompt" data-i18n="[title]Delete prompt"></i>
                                </div>
                            </div>

                            <div>
                                <label for="sysprompt_content" class="flex-container">
                                    <small data-i18n="Prompt Content">Prompt Content</small>
                                    <i class="editor_maximize fa-solid fa-maximize right_menu_button" data-for="sysprompt_content" title="Expand the editor" data-i18n="[title]Expand the editor"></i>
                                </label>
                                <textarea id="sysprompt_content" data-macros class="text_pole textarea_compact autoSetHeight"></textarea>
                            </div>

                            <div>
                                <label for="sysprompt_post_history" class="flex-container">
                                    <small data-i18n="Post-History Instructions">Post-History Instructions</small>
                                    <i class="editor_maximize fa-solid fa-maximize right_menu_button" data-for="sysprompt_post_history" title="Expand the editor" data-i18n="[title]Expand the editor"></i>
                                </label>
                                <textarea id="sysprompt_post_history" data-macros class="text_pole textarea_compact autoSetHeight"></textarea>
                            </div>
                        </div>

                        <div>
                            <h4 class="range-block-title justifyLeft standoutHeader">
                                <span data-i18n="Custom Stopping Strings">
                                    Custom Stopping Strings
                                </span>
                                <a href="https://docs.sillytavern.app/usage/core-concepts/advancedformatting/#custom-stopping-strings" class="notes-link" target="_blank">
                                    <span class="fa-solid fa-circle-question note-link-span"></span>
                                </a>
                            </h4>
                            <div>
                                <small>
                                    <span data-i18n="JSON serialized array of strings">JSON serialized array of strings</span>
                                    <i class="fa-solid fa-question-circle opacity50p" title="e.g: [&quot;Ford&quot;, &quot;BMW&quot;, &quot;Fiat&quot;]"></i>
                                </small>
                            </div>
                            <div>
                                <textarea id="custom_stopping_strings" class="text_pole textarea_compact monospace autoSetHeight"></textarea>
                            </div>
                            <label class="checkbox_label" for="custom_stopping_strings_macro">
                                <input id="custom_stopping_strings_macro" type="checkbox" checked>
                                <small data-i18n="Replace Macro in Stop Strings">
                                    Replace Macro in Stop Strings
                                </small>
                            </label>
                        </div>

                        <div name="tokenizerSettingsBlock" data-cc-null>
                            <div name="tokenizerSelectorBlock">
                                <h4 class="standoutHeader"><span data-i18n="Tokenizer">Tokenizer</span>
                                    <a href="https://docs.sillytavern.app/usage/prompts/tokenizer/" class="notes-link" target="_blank">
                                        <span class="fa-solid fa-circle-question note-link-span"></span>
                                    </a>
                                </h4>
                                <select id="tokenizer">
                                    <option value="99">Best match (recommended)</option>
                                    <option value="0">None / Estimated</option>
                                    <option value="1">GPT-2</option>
                                    <!-- Option #2 was a legacy GPT-2/3 tokenizer -->
                                    <option value="3">Llama 1/2</option>
                                    <option value="12">Llama 3</option>
                                    <option value="13">Gemma / Gemini</option>
                                    <option value="14">Jamba</option>
                                    <option value="15">Qwen2</option>
                                    <option value="16">Command-R</option>
                                    <option value="19">Command-A</option>
                                    <option value="4">NerdStash (NovelAI Clio)</option>
                                    <option value="5">NerdStash v2 (NovelAI Kayra)</option>
                                    <option value="7">Mistral V1</option>
                                    <option value="17">Mistral Nemo</option>
                                    <option value="8">Yi</option>
                                    <option value="11">Claude 1/2</option>
                                    <option value="18">DeepSeek V3</option>
                                    <option value="6">API (WebUI / koboldcpp)</option>
                                </select>
                            </div>
                            <div class="range-block flex-container flexnowrap" name="tokenPaddingBlock">
                                <div class="range-block-title justifyLeft">
                                    <small data-i18n="Token Padding">
                                        Token Padding
                                    </small>
                                </div>
                                <input id="token_padding" class="text_pole textarea_compact" type="number" min="-2048" max="2048" step="1" />
                            </div>
                        </div>
                        <div>
                            <h4 class="standoutHeader">
                                <span data-i18n="Reasoning">Reasoning</span>
                            </h4>
                            <div>
                                <div class="flex-container alignItemsBaseline">
                                    <label class="checkbox_label flex1" for="reasoning_auto_parse" title="Automatically parse reasoning blocks from main content between the reasoning prefix/suffix. Both fields must be defined and non-empty." data-i18n="[title]reasoning_auto_parse">
                                        <input id="reasoning_auto_parse" type="checkbox" />
                                        <small data-i18n="Auto-Parse">
                                            Auto-Parse
                                        </small>
                                    </label>
                                    <label class="checkbox_label flex1" for="reasoning_auto_expand" title="Automatically expand reasoning blocks." data-i18n="[title]reasoning_auto_expand">
                                        <input id="reasoning_auto_expand" type="checkbox" />
                                        <small data-i18n="Auto-Expand">
                                            Auto-Expand
                                        </small>
                                    </label>
                                    <label class="checkbox_label flex1" for="reasoning_show_hidden" title="Show reasoning time for models with hidden reasoning." data-i18n="[title]reasoning_show_hidden">
                                        <input id="reasoning_show_hidden" type="checkbox" />
                                        <small data-i18n="Show Hidden">
                                            Show Hidden
                                        </small>
                                    </label>
                                </div>
                                <div class="flex-container alignItemsBaseline">
                                    <label class="checkbox_label flex1" for="reasoning_add_to_prompts" title="Add existing reasoning blocks to prompts. To add a new reasoning block, use the message edit menu." data-i18n="[title]reasoning_add_to_prompts">
                                        <input id="reasoning_add_to_prompts" type="checkbox" />
                                        <small data-i18n="Add to Prompts">
                                            Add to Prompts
                                        </small>
                                    </label>
                                    <div class="flex1 flex-container alignItemsBaseline" title="Maximum number of reasoning blocks to be added per prompt, counting from the last message." data-i18n="[title]reasoning_max_additions">
                                        <input id="reasoning_max_additions" class="text_pole textarea_compact widthUnset" type="number" min="0" max="999" />
                                        <small data-i18n="Max">Max</small>
                                    </div>
                                </div>
                                <details>
                                    <summary data-i18n="Reasoning Formatting">
                                        Reasoning Formatting
                                    </summary>
                                    <div class="flex-container" title="Select your current Reasoning Template" data-i18n="[title]Select your current Reasoning Template">
                                        <select id="reasoning_select" data-preset-manager-for="reasoning" class="flex1 text_pole"></select>
                                        <div class="flex-container margin0 justifyCenter gap3px">
                                            <input type="file" hidden data-preset-manager-file="reasoning" accept=".json, .settings">
                                            <i data-preset-manager-update="reasoning" class="menu_button fa-solid fa-save" title="Update current template" data-i18n="[title]Update current template"></i>
                                            <i data-preset-manager-rename="reasoning" class="menu_button fa-pencil fa-solid" title="Rename current template" data-i18n="[title]Rename current template"></i>
                                            <i data-preset-manager-new="reasoning" class="menu_button fa-solid fa-file-circle-plus" title="Save template as" data-i18n="[title]Save template as"></i>
                                            <i data-preset-manager-import="reasoning" class="displayNone menu_button fa-solid fa-file-import" title="Import template" data-i18n="[title]Import template"></i>
                                            <i data-preset-manager-export="reasoning" class="displayNone menu_button fa-solid fa-file-export" title="Export template" data-i18n="[title]Export template"></i>
                                            <i data-preset-manager-restore="reasoning" class="menu_button fa-solid fa-recycle" title="Restore current template" data-i18n="[title]Restore current template"></i>
                                            <i data-preset-manager-delete="reasoning" class="menu_button fa-solid fa-trash-can" title="Delete template" data-i18n="[title]Delete template"></i>
                                        </div>
                                    </div>
                                    <div class="flex-container">
                                        <div class="flex1" title="Inserted before the reasoning content." data-i18n="[title]reasoning_prefix">
                                            <small data-i18n="Prefix">Prefix</small>
                                            <textarea id="reasoning_prefix" data-macros class="text_pole textarea_compact autoSetHeight"></textarea>
                                        </div>
                                        <div class="flex1" title="Inserted after the reasoning content." data-i18n="[title]reasoning_suffix">
                                            <small data-i18n="Suffix">Suffix</small>
                                            <textarea id="reasoning_suffix" data-macros class="text_pole textarea_compact autoSetHeight"></textarea>
                                        </div>
                                    </div>
                                    <div class="flex-container">
                                        <div class="flex1" title="Inserted between the reasoning and the message content." data-i18n="[title]reasoning_separator">
                                            <small data-i18n="Separator">Separator</small>
                                            <textarea id="reasoning_separator" data-macros class="text_pole textarea_compact autoSetHeight"></textarea>
                                        </div>
                                    </div>
                                </details>
                            </div>
                        </div>
                        <div>
                            <h4 class="standoutHeader" data-i18n="Miscellaneous">Miscellaneous</h4>
                            <div name="bindModelPresetBlock" data-cc-null>
                                <label for="bind_model_templates" class="checkbox_label">
                                    <input id="bind_model_templates" type="checkbox" />
                                    <small data-i18n="Bind Model to Templates">Bind Model to Templates</small>
                                    <span class="fa-solid fa-circle-question" data-i18n="[title]bind_model_templates_desc" title="When connecting to an API or choosing a model, automatically activate the current Instruct and Context templates if the model name or its chat template matches the currently loaded model."></span>
                                </label>
                            </div>
                            <div>
                                <small>
                                    <span data-i18n="Non-markdown strings">
                                        Non-markdown strings
                                    </span>
                                </small>
                                <div>
                                    <input id="markdown_escape_strings" data-macros class="text_pole textarea_compact" type="text" data-i18n="[placeholder]comma delimited,no spaces between" placeholder="comma delimited,no spaces between" />
                                </div>
                            </div>

                            <div name="startReplyWithBlock">
                                <div>
                                    <small>
                                        <span data-i18n="Start Reply With">
                                            Start Reply With
                                        </span>
                                    </small>
                                    <div>
                                        <textarea id="start_reply_with" data-macros class="text_pole textarea_compact autoSetHeight"></textarea>
                                    </div>
                                    <label class="checkbox_label" for="chat-show-reply-prefix-checkbox">
                                        <input id="chat-show-reply-prefix-checkbox" type="checkbox" />
                                        <small data-i18n="Show reply prefix in chat">
                                            Show reply prefix in chat
                                        </small>
                                    </label>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>`;

export const CHARACTER_DRAWER_VENDOR_MARKUP = String.raw`
                <div id="rm_PinAndTabs">
                    <div id="right-nav-panel-tabs" class="">
                        <div id="rm_button_selected_ch">
                            <h2 class="interactable"></h2>
                        </div>
                        <div id="result_info" class="flex-container" style="display: none;">
                            <div id="result_info_text" title="Token counts may be inaccurate and provided just for reference." data-i18n="[title]Token counts may be inaccurate and provided just for reference.">
                                <div>
                                    <strong id="result_info_total_tokens" title="Total tokens" data-i18n="[title]Total tokens"><span data-i18n="Calculating...">Calculating...</span></strong>&nbsp;<span data-i18n="Tokens">Tokens</span>
                                </div>
                                <div>
                                    <small title="Permanent tokens" data-i18n="[title]Permanent tokens">
                                        (<span id="result_info_permanent_tokens"></span>&nbsp;<span data-i18n="Permanent">Permanent</span>)
                                    </small>
                                </div>
                            </div>
                            <a id="chartokenwarning" class="right_menu_button fa-solid fa-triangle-exclamation" href="https://docs.sillytavern.app/usage/core-concepts/characterdesign/#character-tokens" target="_blank" title="About Token 'Limits'" data-i18n="[title]About Token 'Limits'"></a>
                            <i title="Click for stats!" data-i18n="[title]Click for stats!" class="fa-solid fa-ranking-star right_menu_button rm_stats_button"></i>
                            <i title="Toggle character info panel" data-i18n="[title]Toggle character info panel" id="hideCharPanelAvatarButton" class="fa-solid fa-eye right_menu_button"></i>
                        </div>
                    </div>
                </div>
                <!-- end group peeking cope structure-->

                <div class="scrollableInner">
                    <div name="Solo Char Create/Edit Panel" id="rm_ch_create_block" class="right_menu flex-container flexFlowColumn" style="display: none;">
                        <form id="form_create" action="javascript:void(null);" method="post" enctype="multipart/form-data">
                            <div id="avatar-and-name-block">
                                <div id="name_div">
                                    <input id="character_name_pole" name="ch_name" class="text_pole" data-i18n="[placeholder]Name this character" placeholder="Name this character" value="" autocomplete="off">
                                    <div class="extension_token_counter">
                                        <span data-i18n="extension_token_counter">Tokens:</span> <span data-token-counter="character_name_pole" data-token-permanent="true">counting...</span>
                                    </div>
                                </div>
                                <div class="flex-container flexFlowColumn expander flexNoGap">
                                    <div id="avatar_div" class="avatar_div buttons_block alignitemsflexstart justifySpaceBetween flexnowrap">
                                        <label id="avatar_div_div" class="add_avatar avatar" for="add_avatar_button" title="Click to select a new avatar for this character" data-i18n="[title]Click to select a new avatar for this character">
                                            <img id="avatar_load_preview" src="img/ai4.png" alt="avatar">
                                            <input hidden type="file" id="add_avatar_button" name="avatar" accept="image/*">
                                        </label>
                                        <div class="flex-container" id="avatar_controls">
                                            <div class="form_create_bottom_buttons_block buttons_block">
                                                <div id="rm_button_back" class="menu_button fa-solid fa-left-long "></div>
                                                <!-- <div id="renameCharButton" class="menu_button fa-solid fa-user-pen" title="Rename Character"></div> -->
                                                <div id="favorite_button" class="menu_button fa-solid fa-star" title="Add to Favorites" data-i18n="[title]Add to Favorites"></div>
                                                <input type="hidden" id="fav_checkbox" name="fav" />
                                                <div id="advanced_div" class="menu_button fa-solid fa-book " title="Advanced Definitions" data-i18n="[title]Advanced Definition"></div>
                                                <div id="world_button" class="menu_button fa-solid fa-globe" title="Character Lore&#10;&#10;Click to load&#10;Shift/Alt-click or long-press to open 'Link to World Info' popup" data-i18n="[title]world_button_title"></div>
                                                <div class="chat_lorebook_button menu_button fa-solid fa-passport" title="Chat Lore&#10;&#10;Click to load&#10;Shift/Alt-click or long-press to open 'Link to Chat Lorebook' popup" data-i18n="[title]chat_lorebook_button_title"></div>
                                                <div id="char_connections_button" class="menu_button fa-solid fa-face-smile" title="Connected Personas" data-i18n="[title]Connected Personas"></div>
                                                <div id="export_button" class="menu_button fa-solid fa-file-export " title="Export and Download" data-i18n="[title]Export and Download"></div>
                                                <!-- <div id="set_chat_character_settings" class="menu_button fa-solid fa-scroll" title="Set a chat scenario override"></div> -->
                                                <!-- <div id="set_character_world" class="menu_button fa-solid fa-globe" title="Set a character World Info / Lorebook"></div> -->
                                                <div id="dupe_button" class="menu_button fa-solid fa-clone " title="Duplicate Character" data-i18n="[title]Duplicate Character"></div>
                                                <label for="create_button" id="create_button_label" class="menu_button fa-solid fa-user-check" title="Create Character" data-i18n="[title]Create Character">
                                                    <input type="submit" id="create_button" name="create_button">
                                                </label>
                                                <div id="delete_button" class="menu_button fa-solid fa-skull red_button" title="Delete Character" data-i18n="[title]Delete Character"></div>
                                            </div>
                                            <label class="flex1 height100p" for="char-management-dropdown">
                                                <select id="char-management-dropdown" class="text_pole">
                                                    <option value="default" disabled selected data-i18n="More...">More...</option>
                                                    <option id="set_character_world" data-i18n="Link to World Info">
                                                        Link to World Info
                                                    </option>
                                                    <option id="import_character_info" data-i18n="Import Card Lore">
                                                        Import Card Lore
                                                    </option>
                                                    <option id="set_chat_character_settings" data-i18n="Character Settings Overrides">
                                                        Character Settings Overrides
                                                    </option>
                                                    <option id="convert_to_persona" data-i18n="Convert to Persona">
                                                        Convert to Persona
                                                    </option>
                                                    <option id="renameCharButton" data-i18n="Rename">
                                                        Rename
                                                    </option>
                                                    <option id="character_source" data-i18n="Link to Source">
                                                        Link to Source
                                                    </option>
                                                    <option id="replace_update" data-i18n="Replace / Update">
                                                        Replace / Update
                                                    </option>
                                                    <option id="import_tags" data-i18n="Import Tags">
                                                        Import Tags
                                                    </option>
                                                    <option id="set_as_assistant" data-i18n="Set / Unset as Welcome Page Assistant">
                                                        Set / Unset as Welcome Page Assistant
                                                    </option>
                                                    <!--<option id="dupe_button">
                                                            Duplicate
                                                        </option>
                                                        <option id="export_button">
                                                            Export
                                                        </option>
                                                        <option id="delete_button">
                                                            Delete
                                                        </option>-->
                                                </select>
                                            </label>
                                        </div>
                                    </div>
                                    <div id="tags_div">
                                        <div class="tag_controls">
                                            <input id="tagInput" class="text_pole textarea_compact tag_input wide100p margin0" data-i18n="[placeholder]Search / Create Tags" placeholder="Search / Create tags" />
                                            <div class="tags_view menu_button fa-solid fa-tags" title="View all tags" data-i18n="[title]View all tags"></div>
                                        </div>
                                        <div id="tagList" class="tags"></div>
                                    </div>
                                </div>
                            </div>
                            <div id="spoiler_free_desc" class="inline-drawer flex-container flexFlowColumn flexNoGap">
                                <div class="inline-drawer-toggle inline-drawer-header padding0 gap5px standoutHeader">
                                    <div id="creators_notes_div" class="title_restorable flexGap5 wide100p ">
                                        <span class="flex1" data-i18n="Creator's Notes">Creator's Notes</span>
                                        <div id="creators_note_styles_button" class="margin0 menu_button fa-solid fa-palette fa-fw" title="Allow / Forbid the use of global styles for this character." data-i18n="[title]Allow / Forbid the use of global styles for this character."></div>
                                        <div id="spoiler_free_desc_button" class="margin0 menu_button fa-solid fa-eye fa-fw" title="Show / Hide Description and First Message" data-i18n="[title]Show / Hide Description and First Message"></div>
                                    </div>
                                    <div class="flex-container widthFitContent">
                                        <div class="inline-drawer-icon fa-solid fa-circle-chevron-down down interactable"></div>
                                    </div>
                                </div>
                                <div class="inline-drawer-content">
                                    <div id="creator_notes_spoiler"></div>
                                    <div id="creator_notes_empty" data-i18n="No Creator's Notes provided.">
                                        No Creator's Notes provided.
                                    </div>
                                </div>
                            </div>
                            <small id="creators_note_desc_hidden" data-i18n="Character details are hidden.">Character details are hidden.</small>
                            <div id="descriptionWrapper" class="flex-container flexFlowColumn flex1">
                                <div id="description_div" class="title_restorable">
                                    <div class="flex-container alignitemscenter">
                                        <span data-i18n="Character Description" class="mdhotkey_location">Description</span>
                                        <i class="editor_maximize fa-solid fa-maximize right_menu_button" data-for="description_textarea" title="Expand the editor" data-i18n="[title]Expand the editor"></i>
                                        <a href="https://docs.sillytavern.app/usage/core-concepts/characterdesign/#character-description" class="notes-link" target="_blank">
                                            <span class="fa-solid fa-circle-question note-link-span"></span>
                                        </a>
                                    </div>
                                    <div id="character_open_media_overrides" class="menu_button menu_button_icon open_media_overrides" title="Click to allow/forbid the use of external media for this character." data-i18n="[title]Click to allow/forbid the use of external media for this character.">
                                        <i id="character_media_allowed_icon" class="fa-solid fa-fw fa-link"></i>
                                        <i id="character_media_forbidden_icon" class="fa-solid fa-fw fa-link-slash"></i>
                                        <span data-i18n="Ext. Media">
                                            Ext. Media
                                        </span>
                                    </div>
                                </div>
                                <textarea id="description_textarea" class="mdHotkeys" data-macros data-i18n="[placeholder]Describe your character's physical and mental traits here." placeholder="Describe your character's physical and mental traits here." name="description" placeholder=""></textarea>
                                <div class="extension_token_counter">
                                    <span data-i18n="extension_token_counter">Tokens:</span> <span data-token-counter="description_textarea" data-token-permanent="true">counting...</span>
                                </div>
                            </div>
                            <div id="firstMessageWrapper" class="flex-container flexFlowColumn flex1">
                                <div id="first_message_div" class="title_restorable">
                                    <div class="flex-container alignitemscenter flex1">
                                        <span data-i18n="First message" class="mdhotkey_location">First message</span>
                                        <i class="editor_maximize fa-solid fa-maximize right_menu_button" data-for="firstmessage_textarea" title="Expand the editor" data-i18n="[title]Expand the editor"></i>
                                        <a href="https://docs.sillytavern.app/usage/core-concepts/characterdesign/#first-message" class="notes-link" target="_blank">
                                            <span class="fa-solid fa-circle-question note-link-span"></span>
                                        </a>
                                    </div>
                                    <div class="menu_button menu_button_icon open_alternate_greetings margin0" title="Click to set additional greeting messages" data-i18n="[title]Click to set additional greeting messages">
                                        <span data-i18n="Alt. Greetings">
                                            Alt. Greetings
                                        </span>
                                    </div>
                                </div>
                                <textarea id="firstmessage_textarea" class="mdHotkeys" data-macros data-i18n="[placeholder]This will be the first message from the character that starts every chat." placeholder="This will be the first message from the character that starts every chat." name="first_mes" placeholder=""></textarea>
                                <div class="extension_token_counter">
                                    <span data-i18n="extension_token_counter">Tokens:</span> <span data-token-counter="firstmessage_textarea">counting...</span>
                                </div>
                            </div>
                            <!-- these divs are invisible and used for server communication purposes -->
                            <div id="hidden-divs">
                                <input id="character_json_data" name="json_data" type="hidden">
                                <input id="avatar_url_pole" name="avatar_url" type="hidden">
                                <input id="selected_chat_pole" name="chat" type="hidden">
                                <input id="create_date_pole" name="create_date" type="hidden">
                                <input id="last_mes_pole" name="last_mes" type="hidden">
                                <input id="character_world" name="world" type="hidden">
                            </div>
                            <!-- now back to normal divs for display purposes-->
                        </form>
                    </div>
                    <div name="Group Chat Edit Panel" id="rm_group_chats_block" class="right_menu flex-container flexNoGap">
                        <div class="inline-drawer wide100p flexFlowColumn">
                            <div id="groupControlsToggle" class="inline-drawer-toggle inline-drawer-header">
                                <span>
                                    <span data-i18n="Group Controls">Group Controls</span>
                                    <a href="https://docs.sillytavern.app/usage/core-concepts/groupchats/" class="notes-link" target="_blank">
                                        <span class="fa-solid fa-circle-question note-link-span"></span>
                                    </a>
                                </span>
                                <div class="fa-solid fa-circle-chevron-down inline-drawer-icon down"></div>
                            </div>
                            <div class="inline-drawer-content">
                                <div id="group-metadata-controls" class="marginTopBot5">
                                    <div class="flex-container wide100p">
                                        <input id="rm_group_chat_name" class="text_pole flex1" type="text" name="chat_name" data-i18n="[placeholder]Chat Name (Optional)" placeholder="Chat Name (Optional)" />
                                        <div class="chat_lorebook_button menu_button fa-solid fa-passport" title="Chat Lore&#10;&#10;Click to load&#10;Shift/Alt-click or long-press to open 'Link to Chat Lorebook' popup" data-i18n="[title]chat_lorebook_button_title"></div>
                                    </div>
                                    <label class="flex1 height100p" for="group-chat-lorebook-dropdown">
                                        <select id="group-chat-lorebook-dropdown" class="text_pole">
                                            <option value="default" disabled selected data-i18n="More...">More...</option>
                                            <option id="group_chat_lorebook_link" data-i18n="Link to Chat Lorebook">Link to Chat Lorebook</option>
                                        </select>
                                    </label>
                                    <div id="group_tags_div" class="wide100p">
                                        <div class="tag_controls">
                                            <input id="groupTagInput" class="text_pole textarea_compact tag_input flex1 margin0" data-i18n="[placeholder]Search / Create Tags" placeholder="Search / Create tags" />
                                            <div class="tags_view menu_button fa-solid fa-tags margin0" title="View all tags" data-i18n="[title]View all tags"></div>
                                        </div>
                                        <div id="groupTagList" class="tags paddingTopBot5"></div>
                                    </div>
                                    <div id="rm_group_top_bar" class="flex-container alignitemscenter spaceBetween width100p fontsize80p">
                                        <div>
                                            <label class="add_avatar avatar flex-container justifyCenter" for="group_avatar_button" title="Click to select a new avatar for this group" data-i18n="[title]Click to select a new avatar for this group">
                                                <div id="group_avatar_preview">
                                                    <div class="avatar">
                                                        <img src="img/ai4.png" alt="avatar">
                                                    </div>
                                                </div>
                                                <input hidden type="file" id="group_avatar_button" name="avatar" accept="image/png, image/jpeg, image/jpg, image/gif, image/bmp">
                                            </label>
                                        </div>
                                        <div name="GroupStragegyAndOrder" id="rm_group_buttons" class="flex-container paddingLeftRight5 flex2">
                                            <div class="flex1 flexGap5">
                                                <label for="rm_group_activation_strategy" class="flexnowrap width100p whitespacenowrap">
                                                    <span data-i18n="Group reply strategy">Group reply strategy</span>
                                                </label>
                                                <select id="rm_group_activation_strategy">
                                                    <option value="2" data-i18n="Manual">Manual</option>
                                                    <option value="0" data-i18n="Natural order">Natural order</option>
                                                    <option value="1" data-i18n="List order">List order</option>
                                                    <option value="3" data-i18n="Pooled order">Pooled order</option>
                                                </select>
                                            </div>
                                            <div class="flex1 flexGap5">
                                                <label for="rm_group_generation_mode" class="flexnowrap width100p whitespacenowrap">
                                                    <span data-i18n="Group generation handling mode">Group generation handling mode</span>
                                                </label>
                                                <select id="rm_group_generation_mode">
                                                    <option value="0" data-i18n="Swap character cards">Swap character cards</option>
                                                    <option value="1" data-i18n="Join character cards (exclude muted)">Join character cards (exclude muted)</option>
                                                    <option value="2" data-i18n="Join character cards (include muted)">Join character cards (include muted)</option>
                                                </select>
                                            </div>
                                            <div class="flex1 flexGap5" title="Inserted before each part of the joined fields." data-i18n="[title]Inserted before each part of the joined fields.">
                                                <label for="rm_group_generation_mode_join_prefix" class="flexnowrap width100p whitespacenowrap">
                                                    <span data-i18n="Join Prefix">Join Prefix</span>
                                                    <div class="fa-solid fa-circle-info opacity50p" data-i18n="[title]When 'Join character cards' is selected, all respective fields of the characters are being joined together.This means that in the story string for example all character descriptions will be joined to one big text.If you want those fields to be separated, you can define a prefix or suffix here.This value supports normal macros and will also replace \{{char\}} with the relevant char's name and &lt;FIELDNAME&gt; with the name of the part (e.g.: description, personality, scenario, etc.)" title="When 'Join character cards' is selected, all respective fields of the characters are being joined together.&#13;This means that in the story string for example all character descriptions will be joined to one big text.&#13;If you want those fields to be separated, you can define a prefix or suffix here.&#13;&#13;This value supports normal macros and will also replace \{{char\}} with the relevant char's name and &lt;FIELDNAME&gt; with the name of the part (e.g.: description, personality, scenario, etc.)">
                                                    </div>
                                                </label>
                                                <textarea id="rm_group_generation_mode_join_prefix" class="text_pole wide100p textarea_compact autoSetHeight" placeholder="&mdash;" rows="1"></textarea>
                                            </div>
                                            <div class="flex1 flexGap5" title="Inserted after each part of the joined fields." data-i18n="[title]Inserted after each part of the joined fields.">
                                                <label for="rm_group_generation_mode_join_suffix" class="flexnowrap width100p whitespacenowrap">
                                                    <span data-i18n="Join Suffix">Join Suffix</span>
                                                    <div class="fa-solid fa-circle-info opacity50p" data-i18n="[title]When 'Join character cards' is selected, all respective fields of the characters are being joined together.This means that in the story string for example all character descriptions will be joined to one big text.If you want those fields to be separated, you can define a prefix or suffix here.This value supports normal macros and will also replace \{{char\}} with the relevant char's name and &lt;FIELDNAME&gt; with the name of the part (e.g.: description, personality, scenario, etc.)" title="When 'Join character cards' is selected, all respective fields of the characters are being joined together.&#13;This means that in the story string for example all character descriptions will be joined to one big text.&#13;If you want those fields to be separated, you can define a prefix or suffix here.&#13;&#13;This value supports normal macros and will also replace \{{char\}} with the relevant char's name and &lt;FIELDNAME&gt; with the name of the part (e.g.: description, personality, scenario, etc.)">
                                                    </div>
                                                </label>
                                                <textarea id="rm_group_generation_mode_join_suffix" class="text_pole wide100p textarea_compact autoSetHeight" placeholder="&mdash;" rows="1"></textarea>
                                            </div>
                                        </div>
                                        <div id="GroupFavDelOkBack" class="flex-container flexGap5 spaceEvenly flex1">
                                            <div id="rm_button_back_from_group" class="heightFitContent margin0 menu_button fa-solid fa-fw fa-left-long"></div>
                                            <div id="rm_group_scenario" class="heightFitContent margin0 menu_button fa-solid fa-fw fa-scroll" title="Set group chat character settings overrides" data-i18n="[title]Set group chat character settings overrides"></div>
                                            <div id="group_favorite_button" class="heightFitContent margin0 menu_button fa-solid fa-fw fa-star" title="Add to Favorites" data-i18n="[title]Add to Favorites"></div>
                                            <input id="rm_group_fav" type="hidden" />
                                            <div id="group_open_media_overrides" class="heightFitContent margin0 menu_button menu_button_icon open_media_overrides" title="Click to allow/forbid the use of external media for this group." data-i18n="[title]Click to allow/forbid the use of external media for this group.">
                                                <i id="group_media_allowed_icon" class="fa-solid fa-fw fa-link"></i>
                                                <i id="group_media_forbidden_icon" class="fa-solid fa-fw fa-link-slash"></i>
                                            </div>
                                            <div id="rm_group_submit" class="heightFitContent margin0 menu_button fa-solid fa-fw fa-check" title="Create" data-i18n="[title]Create"></div>
                                            <div id="rm_group_restore_avatar" class="heightFitContent margin0 menu_button fa-solid fa-fw fa-images" title="Restore collage avatar" data-i18n="[title]Restore collage avatar"></div>
                                            <div id="rm_group_delete" class="heightFitContent margin0 menu_button fa-solid fa-fw fa-trash-can" title="Delete" data-i18n="[title]Delete"></div>
                                            <div class="flex1">
                                                <label class="checkbox_label whitespacenowrap">
                                                    <input id="rm_group_allow_self_responses" type="checkbox" />
                                                    <span data-i18n="Allow self responses">Allow self responses</span>
                                                </label>
                                                <label id="rm_group_automode_label" class="checkbox_label whitespacenowrap">
                                                    <input id="rm_group_automode" type="checkbox" />
                                                    <span data-i18n="Auto Mode">Auto Mode</span>
                                                    <input id="rm_group_automode_delay" class="text_pole textarea_compact widthUnset" type="number" min="1" max="999" step="1" value="5" title="Auto Mode delay" data-i18n="[title]Auto Mode delay" />
                                                </label>
                                                <label id="rm_group_hidemutedsprites_label" class="checkbox_label whitespacenowrap">
                                                    <input id="rm_group_hidemutedsprites" type="checkbox" />
                                                    <span data-i18n="Hide Muted Member Sprites">Hide Muted Member Sprites</span>
                                                </label>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="inline-drawer wide100p flexFlowColumn">
                            <div id="groupCurrentMemberListToggle" class="inline-drawer-toggle inline-drawer-header">
                                <span data-i18n="Current Members">Current Members </span><i id="groupCurrentMemberPopoutButton" class="fa-solid fa-window-restore menu_button"></i>
                                <div class="fa-solid fa-circle-chevron-down inline-drawer-icon down"></div>
                            </div>
                            <div class="inline-drawer-content">
                                <div id="currentGroupMembers" name="Current Group Members" class="flex-container flexFlowColumn overflowYAuto flex1">
                                    <div id="rm_group_members_header">
                                        <input id="rm_group_members_filter" class="text_pole margin0" type="search" data-i18n="[placeholder]Search..." placeholder="Search..." />
                                    </div>
                                    <div class="rm_tag_controls">
                                        <div class="tags rm_tag_filter"></div>
                                    </div>
                                    <div id="rm_group_members_pagination" class="rm_group_members_pagination group_pagination"></div>
                                    <div id="rm_group_members" class="rm_group_members overflowYAuto flex-container" group_empty_text="Group is empty." data-i18n="[group_empty_text]Group is empty."></div>
                                </div>
                            </div>
                        </div>
                        <div class="inline-drawer wide100p flexFlowColumn">
                            <div id="groupAddMemberListToggle" class="inline-drawer-toggle inline-drawer-header">
                                <span data-i18n="Add Members">Add Members</span>
                                <div class="fa-solid fa-circle-chevron-down inline-drawer-icon down"></div>
                            </div>
                            <div class="inline-drawer-content">
                                <div id="unaddedCharList" name="Unadded Char List" class="flex-container flexFlowColumn overflowYAuto flex1">
                                    <div id="rm_group_add_members_header">
                                        <input id="rm_group_filter" class="text_pole margin0" type="search" data-i18n="[placeholder]Search..." placeholder="Search..." />
                                    </div>
                                    <div class="rm_tag_controls">
                                        <div class="tags rm_tag_filter"></div>
                                    </div>
                                    <div id="rm_group_add_members_pagination" class="group_pagination"></div>
                                    <div id="rm_group_add_members" class="overflowYAuto flex-container" no_characters_text="No characters available" data-i18n="[no_characters_text]No characters available"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div id="rm_character_import" class="right_menu" style="display: none;">
                        <form id="form_import" action="javascript:void(null);" method="post" enctype="multipart/form-data">
                            <input multiple type="file" id="character_import_file" accept=".json, image/png, .yaml, .yml, .charx, .byaf" name="avatar">
                            <input id="character_import_file_type" name="file_type" class="text_pole" value="" autocomplete="off">
                        </form>
                        <input type="file" id="character_replace_file" accept=".json, image/png, .yaml, .yml, .charx, .byaf" name="replace_avatar" hidden>
                    </div>
                    <div name="Character List Panel" id="rm_characters_block" class="right_menu">
                        <div id="charListFixedTop">
                            <div id="rm_button_bar">
                                <div id="rm_button_create" title="Create New Character" data-i18n="[title]Create New Character" class="menu_button fa-solid fa-user-plus"></div>
                                <div id="character_import_button" title="Import Character from File" data-i18n="[title]Import Character from File" class="menu_button fa-solid fa-file-import"></div>
                                <div id="external_import_button" title="Import content from external URL" data-i18n="[title]Import content from external URL" class="menu_button fa-solid fa-cloud-arrow-down"></div>
                                <div id="rm_button_group_chats" title="Create New Chat Group" data-i18n="[title]Create New Chat Group" class="menu_button fa-solid fa-users-gear"></div>
                                <div id="rm_buttons_container">
                                    <!-- Container for additional buttons added by extensions -->
                                </div>
                                <select id="character_sort_order" class="flex1 text_pole textarea_compact" title="Characters sorting order" data-i18n="[title]Characters sorting order">
                                    <option data-field="search" data-order="desc" data-i18n="Search" hidden>Search</option>
                                    <option data-field="name" data-order="asc" data-i18n="A-Z">A-Z</option>
                                    <option data-field="name" data-order="desc" data-i18n="Z-A">Z-A</option>
                                    <option data-field="create_date" data-order="desc" data-i18n="Newest">Newest</option>
                                    <option data-field="create_date" data-order="asc" data-i18n="Oldest">Oldest</option>
                                    <option data-field="fav" data-order="desc" data-rule="boolean" data-i18n="Favorites">Favorites</option>
                                    <option data-field="date_last_chat" data-order="desc" data-i18n="Recent">Recent</option>
                                    <option data-field="chat_size" data-order="desc" data-i18n="Most chats">Most chats</option>
                                    <option data-field="chat_size" data-order="asc" data-i18n="Least chats">Least chats</option>
                                    <option data-field="data_size" data-order="desc" data-i18n="Most tokens">Most tokens</option>
                                    <option data-field="data_size" data-order="asc" data-i18n="Least tokens">Least tokens</option>
                                    <option data-field="name" data-order="random" data-i18n="Random">Random</option>
                                </select>
                                <div id="rm_button_search" class="right_menu_button fa-fw fa-solid fa-search" title="Toggle search bar" data-i18n="[title]Toggle search bar"></div>
                            </div>
                            <div id="form_character_search_form">
                                <input id="character_search_bar" class="text_pole textarea_compact width100p" type="search" data-i18n="[placeholder]Search..." placeholder="Search..." />
                            </div>
                            <div class="rm_tag_controls">
                                <div class="tags rm_tag_filter"></div>
                                <div class="tags rm_tag_bogus_drilldown"></div>
                            </div>
                        </div>

                        <div id="rm_print_characters_pagination">
                            <i id="charListGridToggle" class="fa-solid fa-table-cells-large menu_button" title="Toggle character grid view" data-i18n="[title]Toggle character grid view"></i>
                            <i id="bulkEditButton" class="fa-solid fa-edit menu_button bulkEditButton" title="Bulk edit characters&#13;&#13;Click to toggle characters&#13;Shift + Click to select/deselect a range of characters&#13;Right-click for actions" data-i18n="[title]Bulk_edit_characters"></i>
                            <div id="bulkSelectedCount" class="bulkEditOptionElement paginationjs-nav"></div>
                            <i id="bulkSelectAllButton" class="fa-solid fa-check-double menu_button bulkEditOptionElement bulkSelectAllButton" title="Bulk select all characters" data-i18n="[title]Bulk select all characters" style="display: none;"></i>
                            <i id="bulkDeleteButton" class="fa-solid fa-trash menu_button bulkEditOptionElement bulkDeleteButton" title="Bulk delete characters" data-i18n="[title]Bulk delete characters" style="display: none;"></i>
                        </div>
                        <div id="rm_print_characters_block" class="flexFlowColumn"></div>
                    </div>
                </div>`;
