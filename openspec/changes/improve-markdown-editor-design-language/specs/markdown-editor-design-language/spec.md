# markdown-editor-design-language Specification

## ADDED Requirements

### Requirement: Application styles SHALL use a shared semantic token system

The application SHALL define shared semantic design tokens for surfaces, text, borders, accents, interactive states, focus treatment, radius, spacing, and control sizes. Primary editor-shell and QuickPick styling paths SHALL consume semantic tokens instead of hardcoded color literals or duplicated legacy aliases.

#### Scenario: Qt control style uses semantic token

- **GIVEN** a Qt control style is used on the editor shell, QuickPick, sidebar, tabs, splitters, scrollbars, buttons, or inputs
- **WHEN** the style defines color, border, radius, focus, hover, pressed, selected, or disabled state
- **THEN** the value is derived from a semantic token
- **AND** the style does not introduce a new hardcoded primary blue or neutral gray

#### Scenario: Legacy alias remains for compatibility

- **GIVEN** an older call site still imports a legacy color alias
- **WHEN** the application runs
- **THEN** the alias resolves to the shared semantic token or underlying canonical color
- **AND** the alias is not treated as a separate source of truth

#### Scenario: Duplicated style definition exists

- **GIVEN** two constants define the same control, such as a titlebar or button style
- **WHEN** one definition shadows the other
- **THEN** the shadowed or duplicate definition is removed or renamed as legacy-only
- **AND** the active application path has one authoritative style definition

#### Scenario: Non-editor pages remain bounded

- **GIVEN** settings, import, history, or other non-editor pages consume existing shared styles
- **WHEN** semantic tokens are introduced for the editor design language
- **THEN** those pages keep their existing layout and interaction behavior
- **AND** only minimal compatibility changes, such as replacing obvious legacy primary colors with aliases, are applied outside the editor shell and QuickPick scope

### Requirement: Interactive components SHALL expose consistent visual states

The application SHALL provide consistent default, hover, pressed, selected, current, focus, and disabled visual states for editor-related controls.

#### Scenario: QuickPick item state changes

- **GIVEN** a QuickPick item is displayed in the document tree
- **WHEN** the item is hovered, selected, or represents the current document
- **THEN** each state is visually distinct
- **AND** the current document has an explicit marker such as a 2px accent indicator or an equivalent code-reviewable affordance

#### Scenario: Keyboard focus is present

- **GIVEN** a user navigates with keyboard focus through search, toolbar, or action buttons
- **WHEN** a control receives focus
- **THEN** a visible focus treatment is shown
- **AND** the focus treatment is not confused with hover or selected state
- **AND** Qt QSS implementations use supported mechanisms such as border, background, padding, or control-specific state styling rather than relying on unsupported Web CSS `outline` semantics

#### Scenario: Disabled state is present

- **GIVEN** a toolbar button or action button is unavailable
- **WHEN** the control is disabled
- **THEN** the disabled state lowers contrast and removes active accent affordance
- **AND** hover does not make the control appear clickable

### Requirement: Cherry Markdown SHALL be visually bridged to MarkRender tokens

The Markdown editor plugin SHALL map Cherry Markdown CSS variables to MarkRender theme variables so that the WebView editor and Qt shell share the same design language.

#### Scenario: Runtime CSS contains theme bridge

- **GIVEN** `app/editor/plugins/markdown/index.html` loads the Markdown editor CSS
- **WHEN** the loaded CSS chain is inspected
- **THEN** the MarkRender theme bridge is present in the runtime-loaded CSS file or in a stylesheet loaded after Cherry CSS
- **AND** the bridge is not present only in an unused source CSS file

#### Scenario: Cherry primary color is mapped

- **GIVEN** Cherry Markdown renders toolbar, editor, previewer, links, cursor, selection, or dropdown UI
- **WHEN** the CSS computes primary, border, background, or text colors
- **THEN** those values come from MarkRender theme variables
- **AND** Cherry does not visually introduce an unrelated blue or gray palette

#### Scenario: Body background uses theme variable

- **GIVEN** the Markdown plugin HTML is loaded in QWebEngineView
- **WHEN** the page body renders
- **THEN** its background is derived from the MarkRender theme variable
- **AND** it does not hardcode white independently of the application shell

#### Scenario: Theme bridge is centralized

- **GIVEN** a developer needs to adjust Markdown editor colors
- **WHEN** they inspect the Markdown plugin CSS loaded at runtime
- **THEN** MarkRender-specific overrides are grouped in a theme bridge block or equivalent centralized section
- **AND** the developer does not need to edit many unrelated Cherry rules to change the palette

### Requirement: Markdown preview typography SHALL prioritize long-form readability

The Markdown preview SHALL render prose, headings, lists, blockquotes, code, links, and tables with readable rhythm, controlled line breaks, and semantic styling.

#### Scenario: Mixed-language prose wraps naturally

- **GIVEN** a Markdown document contains Chinese, English, inline code, and links
- **WHEN** the preview renders the document
- **THEN** normal prose does not use global `word-break: break-all`
- **AND** long links or long tokens remain contained without breaking ordinary words unnaturally

#### Scenario: Heading rhythm is readable

- **GIVEN** a Markdown document contains H1 through H4 headings
- **WHEN** the preview renders headings
- **THEN** heading line-height supports multi-line headings without crowding
- **AND** heading top and bottom margins create clear section rhythm

#### Scenario: Blockquote is calm and document-like

- **GIVEN** a Markdown document contains a blockquote
- **WHEN** the preview renders the blockquote
- **THEN** the leading border is no wider than 4px
- **AND** background and text colors are neutral or informational, not warning-like
- **AND** nested paragraph spacing remains readable

#### Scenario: Code styling avoids error semantics

- **GIVEN** a Markdown document contains inline code and fenced code blocks
- **WHEN** the preview renders code
- **THEN** inline code uses a neutral code style
- **AND** code block background, radius, padding, and font size are consistent with MarkRender typography tokens
- **AND** default inline code color is not the error semantic color

#### Scenario: Table styling has its own semantics

- **GIVEN** a Markdown document contains a table
- **WHEN** the preview renders the table
- **THEN** header background, border, padding, and row rhythm use table-specific tokens or styles
- **AND** table header background does not merely reuse inline-code background

### Requirement: Markdown toolbar SHALL feel native to the editor shell

The Cherry toolbar SHALL use MarkRender control sizing, state colors, grouping, focus, and active state rules so it reads as part of the desktop editor.

#### Scenario: Toolbar button hover and active states

- **GIVEN** the Markdown toolbar is visible
- **WHEN** a user hovers or activates a toolbar button
- **THEN** hover and active states use the shared state matrix
- **AND** active mode buttons such as preview toggle or code theme are distinguishable from transient hover

#### Scenario: Toolbar grouping is low-noise

- **GIVEN** toolbar buttons are grouped by function
- **WHEN** groups render
- **THEN** grouping is expressed primarily through spacing or subtle separators
- **AND** separators do not dominate the toolbar visually

#### Scenario: Toolbar elevation is restrained

- **GIVEN** the toolbar sits above the editor and previewer
- **WHEN** the toolbar renders
- **THEN** it uses a subtle divider or restrained elevation
- **AND** it uses MarkRender theme variables rather than an unrelated third-party shadow or border treatment

### Requirement: QuickPick SHALL present documents as a polished navigation surface

The QuickPick panel SHALL prioritize document identity and current location over file-type decoration. Search, create action, tree container, and tree items SHALL share one visual vocabulary.

#### Scenario: Document title has priority over icon decoration

- **GIVEN** a QuickPick tree item has an icon, title, and timestamp
- **WHEN** the item renders
- **THEN** the title is the dominant information
- **AND** the icon background does not visually overpower the title

#### Scenario: Item dividers are not visually noisy

- **GIVEN** multiple QuickPick items are listed
- **WHEN** the tree renders
- **THEN** item separation is achieved through spacing, grouping, or subtle boundaries
- **AND** every row does not require a strong full-width divider

#### Scenario: Delegate owns item state visuals

- **GIVEN** QuickPick uses a custom delegate and QTreeWidget stylesheet
- **WHEN** hover, selected, or current states are rendered
- **THEN** the delegate owns the primary item state visuals
- **AND** QSS is limited to container-level styling or non-conflicting fallback rules
- **AND** QSS does not define conflicting item background or text rules for selected/current/hover states

#### Scenario: Search and create controls are visually related

- **GIVEN** the QuickPick search input and create action button sit in the same row
- **WHEN** the panel renders
- **THEN** both controls share compatible height, radius, border, hover, pressed, and focus states

### Requirement: Create action SHALL open a complete creation menu

The primary create action in QuickPick SHALL align its icon, tooltip, and behavior. It SHALL open a menu that preserves access to creating Markdown documents, Excalidraw canvases, and folders.

#### Scenario: Primary create opens a menu

- **GIVEN** the user clicks the primary create action in QuickPick
- **WHEN** the action runs
- **THEN** the existing create menu behavior is invoked or equivalently reproduced
- **AND** the user can choose New Markdown, New Canvas, or New Folder
- **AND** no single create type is silently executed before the user chooses a menu item

#### Scenario: Tooltip matches menu behavior

- **GIVEN** the primary create button is visible
- **WHEN** the user reads its tooltip
- **THEN** the tooltip describes a general create menu or new-item action
- **AND** it does not say “New Folder” when the button opens a broader create menu

#### Scenario: Folder creation remains reachable

- **GIVEN** a user previously used the primary create button to create folders
- **WHEN** the new create menu is opened
- **THEN** New Folder remains available from that menu
- **AND** existing secondary folder creation paths, such as context menu entries, continue to work if present

### Requirement: Visual polish SHALL NOT regress editor behavior

Design-language changes SHALL preserve existing editor workflows and targeted persistence/navigation guarantees.

#### Scenario: Markdown editing workflow still works

- **GIVEN** a user opens an existing Markdown document
- **WHEN** the user edits content, switches to another document, closes the app, and reopens it
- **THEN** the edited content is preserved
- **AND** the visual style changes do not cause an empty-content save or navigation overwrite

#### Scenario: QuickPick workflows still work

- **GIVEN** the user uses QuickPick search, selection, right-click menu, and drag/drop
- **WHEN** the design polish is applied
- **THEN** those interactions remain available
- **AND** hover, selected, current, and focus visuals do not block interaction hit areas

#### Scenario: Targeted tests protect non-visual behavior

- **GIVEN** this design-language change is implemented
- **WHEN** targeted tests run
- **THEN** tests cover at least create action behavior, runtime CSS bridge loading, and any token/style helper behavior that can be tested without GUI screenshot comparison
- **AND** existing persistence and navigation targeted tests continue passing

#### Scenario: Screenshot testing is not required for MVP

- **GIVEN** this change is implemented as an MVP design-language convergence
- **WHEN** verification is planned
- **THEN** automated tests focus on behavior, style helper output, selectors, and runtime asset wiring
- **AND** screenshot regression infrastructure is not required by this change
